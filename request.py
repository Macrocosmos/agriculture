import json
import requests
import rasterio
import numpy as np

API_ENDPOINT = 'http://localhost:8000/api/v1/images/'
SHAPEFILE = './fixtures/raseiniai.geojson'

def band_image(band):
    data = {
        'area': json.loads(open(SHAPEFILE).read()),
        'date': '2017-8-21',
        'take': '0',
        'band': band,
    }

    response = requests.post(url = API_ENDPOINT, data = json.dumps(data))
    return rasterio.io.MemoryFile(response.content)

red_band = band_image('08')
nir_band = band_image('08')

with rasterio.open(red_band) as red_raster_file:
    with rasterio.open(nir_band) as nir_raster_file:
        red = np.array(red_raster_file.read(1), dtype=float)
        nir = np.array(nir_raster_file.read(1), dtype=float)
        print(red)

        num = nir - red
        denom = (nir + red) + 0.00000000001
        ndvi = np.divide(num,denom)

        # ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
        print(ndvi.min(), ndvi.max())
        stretched_ndvi = (ndvi + 1) * 255

        kwargs = red_raster_file.meta
        kwargs.update(dtype = rasterio.uint8, count = 1)

        # profile = red_raster_file.meta
        # profile.update(driver='GTiff')
        # profile.update(dtype=rasterio.float32)

        with rasterio.open('out-ndvi.tif', 'w', **kwargs) as dst:
            dst.write(stretched_ndvi.astype(rasterio.uint8))

        print('succ')
