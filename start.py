from os import environ
from datetime import date, datetime, timedelta
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

api = SentinelAPI(environ.get('SENTINEL_USER'), environ.get('SENTINEL_PASSWORD'), 'https://scihub.copernicus.eu/dhus')

footprint = geojson_to_wkt(read_geojson('fixtures/arskainiai.geojson'))
products = api.query(footprint,
                     initial_date = 'NOW-10DAY',
                     end_date='NOW',
                     platformname = 'Sentinel-2')

print products
api.download_all(products)

print "It's all about the fields."
