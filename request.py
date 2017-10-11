import json
import requests
import rasterio
import urllib.parse
# import rasterio.io
# import io

API_ENDPOINT = 'http://localhost:8000/api/v1/images/'
SHAPEFILE = './fixtures/raseiniai.geojson'

def band_image_url(band):
    data = {
        'area': json.loads(open(SHAPEFILE).read()),
        'date': '2017-8-21',
        'take': '0',
        'band': band,
    }

    url_parts = list(urllib.parse.urlparse(API_ENDPOINT))
    url_parts[4] = urllib.parse.urlencode(data)
    print(urllib.parse.urlunparse(url_parts))
    return urllib.parse.urlunparse(url_parts)

# nir = band_image_url('08')

# n = rasterio.io.MemoryFile(nir)
# print(dir(rasterio))
# f= io.BytesIO(nir)

# with f.open() as fi:
with rasterio.open(band_image_url('08')) as nir_raster_file:
    print('yo')
