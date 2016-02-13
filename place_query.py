from bokeh.embed import components
import simplejson as json
import numpy as np
import pandas as pd
from requests import Session
from collections import namedtuple
import operator


# Read in all API keys
with open("../secrets/google_secrets.json.nogit") as fh: 
  secrets = json.loads(fh.read())

google_api_key = secrets['server_api_key']

Summary = namedtuple('Summary',
      ['count','count_rating','sum_rating','sum_rating_sq',
      'count_price_level','sum_price_level','sum_price_level_sq']
    )

def google_places_parser(resp):
  
  if False:
    print resp.json()['results'][0]
  
  count = 0
  count_rating = 0
  sum_rating = 0
  sum_rating_sq = 0
  count_price_level = 0
  sum_price_level = 0
  sum_price_level_sq = 0

  for r in resp.json()['results']:
    rating = r.get('rating')
    if rating:
      count_rating += 1
      sum_rating += float(rating)
      sum_rating_sq += float(rating)**2

    price_level = r.get('price_level')
    if price_level:
      count_price_level += 1
      sum_price_level += float(price_level)    
      sum_price_level_sq += float(price_level)**2    
    
    count += 1

  summary = Summary(count,count_rating,sum_rating,sum_rating_sq,
                   count_price_level,sum_price_level,sum_price_level_sq)

  return (resp.json().get('next_page_token',''), summary)


def add_tuples(a,b):
  out_list = []
  for i in xrange(min(len(a),len(b))):
    out_list.append(a[i]+b[i])

  return tuple(out_list)


def make_request(lat_lng,amen_query):
  base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
  with Session() as s:
    npt = ''  
    i = 0
    summary = Summary(0,0,0,0,0,0,0)
    while i < 3:
      i+=1 
      if npt == '':
        search_payload = {"key":google_api_key,
                          "radius":1000,
                          "types":amen_query,
                          "location":lat_lng}
      else:
        '''Including a page token forces Google to ignore all other
        search parameters'''
        search_payload = {"key":google_api_key,
                          'pagetoken':npt}

      resp = s.get(base_url, params=search_payload)
      npt, this_summary = google_places_parser(resp)
     
      print this_summary, summary
      summary = summary + this_summary
      if npt == '': break

  return summary

def summarizer(x):
  '''x is a Summary namedtuple'''
  nr = np.float64(x.count_rating)
  mu_r = x.sum_rating/nr
  sd_r = np.sqrt(x.sum_rating_sq/nr - mu_r**2)
  npl = np.float64(x.count_price_level)
  mu_p = x.sum_price_level/npl
  sd_p = np.sqrt(x.sum_price_level_sq/npl - mu_p**2)
  
  return (x.count,x.count_rating,mu_r,sd_r,x.count_price_level,mu_p,sd_p) 


def make_all_requests():
  print make_request('38.9252905465,-76.9797563101','restaurant')
  

if __name__ == "__main__":
  make_all_requests()
