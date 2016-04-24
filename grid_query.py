import simplejson as json
import numpy as np
import pandas as pd
from requests import Session, Request
from requests_futures.sessions import FuturesSession
from itertools import izip, repeat, chain
import time

    

def google_places_json_parser(google_json):
  """ Parses Google Places API JSON result according to predefined template

  Args:
    google_json: JSON object from Google Places API

  Returns:
    records: list of dicts specifying key-value pairs
  
  """
  # now loop over all json results and pull the desired fields
  records = []  
  for r in google_json['results']:
    r['lat'] = r['geometry']['location']['lat']
    r['lng'] = r['geometry']['location']['lng']
    r['num_photos'] = len(r.get('photos',[]))

    records.append( {k:v for k,v in r.iteritems() 
      if k not in ['geometry','icon','opening_hours','photos','scope',
        'reference']} )

  return records


def google_places_callback(sess, resp):
  """ Background callback function for the FuturesSession.get parallelized
  request to the Google places API

  Args:
    sess: FuturesSession object
    resp: response object returned from request

  Returns:
    nothing; instead assigns resp.data
  
  """

  # check that the request returned correctly
  if resp.json()['status'] != "OK":
    resp.data = ('',[])
    return

  # parse the response
  records = google_places_json_parser(resp.json())

  # assign the output to resp.data
  resp.data = (resp.json().get('next_page_token',''), records)



def get_local_amenities(google_api_key,lat_lng_strs,amenity, radius=1000):
  """ Queries Google Places API for amenities within radius meters
  and stores their attributes in a dataframe 
  
  Args:
    google_api_key: the google api key access string
    lat_lng_strs: list of comma delimited lat/lng strings
    amenity: name of the Google Place 'type' parameter
    radius: search radius in meters

  Returns:
    pandas dataframe with place attributes 

  """
  def make_urls(lat_lng_or_npt, flag):
    """ Helper function to generate query URLs from a series 
    of next-page tokens and distinct amenity types

    Args:
      lat_lng_or_npt: either a list of next lat_lng strings or
        a list of of next_page_tokens, depending on flag
      flag: False if first argument is lat_lng, True if npt

    Returns:
      urls: a list of urls
    """

    base_url = ("https://maps.googleapis.com/maps/api/" + 
        "place/nearbysearch/json")

    # create a requests Session to do the formatting
    s = Session()

    urls = []
    for val in lat_lng_or_npt:
      if flag:
        # including a page token forces Google to ignore other parameters
        search_payload = {"key":google_api_key,
                          'pagetoken':val}
      else:
        search_payload = {"key":google_api_key,
                          "radius":radius,
                          "types":amenity,
                          "location":val}

      req = Request('GET', base_url, params=search_payload)
      urls.append(s.prepare_request(req).url)

    return urls


  session = FuturesSession(max_workers=3)

  # input_list can be either a list of lat_lng strings or next_page_tokens
  input_list = lat_lng_strs 
  is_page_tokens = False

  # store all the records
  all_records = []

  # Google permits at most 3 queries returning up to 20 results each 
  for i in xrange(3):
    urls = make_urls(input_list, is_page_tokens)
    results = ( session.get(url,background_callback=google_places_callback)
               for url in urls )
    print(results)

    npts, records = zip(*(x.result().data for x in results))
    input_list = [s for s in npts if s != '']
    is_page_tokens = True
    
    
    all_records += list(chain(*records))

    if len(input_list) == 0:
      break
    time.sleep(2) # delay because next page is not immediately available

  df = pd.DataFrame.from_records(all_records)

  #return df
  return all_records

if __name__ == "__main__":
  lat_lng_strs = '38.939320,-77.059950'
  get_local_amenities(google_api_key,lat_lng_strs)
