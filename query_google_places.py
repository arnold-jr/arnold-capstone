import simplejson as json
from requests import Request, Session
import pandas as pd
from multiprocessing import Pool
from ediblepickle import checkpoint
from requests_futures.sessions import FuturesSession



# Read in all API keys
with open("../secrets/google_secrets.json.nogit") as fh:
    secrets = json.loads(fh.read())
google_api_key = secrets['server_api_key']

# Define amenity types of interest
amenity_types = ['bakery','bar','cafe','grocery_or_supermarket','movie_theater',
            'park','pharmacy','restaurant','spa','subway_station']

def google_places_parser(sess,resp):
  row_dict = {}
  for r in resp.json()['results']:
    loc = r['geometry']['location']
    price_rate_str = '__price_'+str(r.get('price_level'))+'__rating_'+str(r.get('rating'))
    for t in r.get('types'):
      if t in amenity_types:
        key = t+price_rate_str
        if key in row_dict:
          row_dict[key] += 1
        else:
          row_dict[key] = 1

  resp.data = row_dict

@checkpoint(key='parsed_attrs_list.csv', work_dir='data', refresh=False)
def get_all_amenities():
  df = pd.read_hdf('data/df_wo_goog.hd5','df')
  search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
  search_payload = {"key":google_api_key,
                    "radius":1000,
                    "types":'|'.join(amenity_types)}
  urls = (search_url+'?location='+lat_lng_str for lat_lng_str in df['lat_lng'])


  session = FuturesSession(max_workers=7)
  futures = [session.get(url,params=search_payload,
                background_callback=google_places_parser) for url in urls]
  
  return [f.result().data for f in futures]

if __name__ == '__main__':
  get_all_amenities()


