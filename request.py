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

dates = '2017-10-2'

spring = '3-15'
summer = '8-3'
autumn = '10-3'
red_band = band_image('04')
nir_band = band_image('08')

with rasterio.open(red_band) as red_raster_file:
    with rasterio.open(nir_band) as nir_raster_file:
        red = red_raster_file.read(1)
        nir = nir_raster_file.read(1)

        ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
        ndvi[ndvi<0.5] = 0
        ndvi[ndvi>0.8] = 0

        profile = red_raster_file.meta
        profile.update(driver='GTiff')
        profile.update(dtype=rasterio.float32)

        with rasterio.open('thing.tif', 'w', **profile) as dst:
            print(dst.shape)
            print(ndvi.shape)
            print(dst.indexes)
            dst.write(ndvi.astype(rasterio.float32), 1)

        # # ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
        # print(ndvi.min(), ndvi.max())
        # stretched_ndvi = (ndvi + 1) * 255
        #
        # kwargs = red_raster_file.meta
        # kwargs.update(dtype = rasterio.uint8, count = 1)
        #
        # # profile = red_raster_file.meta
        # # profile.update(driver='GTiff')
        # # profile.update(dtype=rasterio.float32)
        #
        # with rasterio.open('out-ndvi.tif', 'w', **kwargs) as dst:
        #     dst.write(stretched_ndvi.astype(rasterio.uint8))

        print('succ')
