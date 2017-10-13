import json
import requests
import rasterio
import numpy as np

API_ENDPOINT = 'http://localhost:8000/api/v1/images/'
SHAPEFILE = './fixtures/raseiniai.geojson'

def band_image(band, date):
    data = {
        'area': json.loads(open(SHAPEFILE).read()),
        'date': date,
        'take': '0',
        'band': band,
    }

    response = requests.post(url = API_ENDPOINT, data = json.dumps(data))
    return rasterio.io.MemoryFile(response.content)

def get_ndvi(red_band, nir_band):
    with rasterio.open(red_band) as red_raster_file:
        with rasterio.open(nir_band) as nir_raster_file:
            red = red_raster_file.read(1)
            nir = nir_raster_file.read(1)
            ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
            # ndvi[ndvi<0.5] = 0
            # ndvi[ndvi>0.8] = 0

            return ndvi


spring = '2017-3-16'
summer = '2017-8-11'
autumn = '2017-10-2'
dates = [spring, summer, autumn]

ndvis = []
for date in dates:
    red_band = band_image('04', date)
    nir_band = band_image('08', date)

    ndvis.append(get_ndvi(red_band, nir_band))

# ndvi_avg = (ndvis[0] + ndvis[2])  / 2.0

ndvi = ndvis[1] - ndvis[2]
ndvi[ndvi<0.3] = 0
# ndvi[ndvi>0.8] = 0

with rasterio.open(band_image('04', '2017-3-16')) as red_file:
    profile = red_file.meta
    profile.update(driver='GTiff')
    profile.update(dtype=rasterio.float32)

with rasterio.open('thing.tif', 'w', **profile) as dst:
    print(dst.shape)
    print(ndvi.shape)
    print(dst.indexes)
    dst.write(ndvi.astype(rasterio.float32), 1)
