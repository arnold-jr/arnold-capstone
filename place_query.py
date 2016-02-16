import simplejson as json
import numpy as np
import pandas as pd
from requests import Session, Request
from requests_futures.sessions import FuturesSession
from collections import namedtuple
import operator
from itertools import izip, repeat
import time


Summary = namedtuple('Summary',
      ['count','count_rating','sum_rating','sum_rating_sq',
      'count_price_level','sum_price_level','sum_price_level_sq']
    ) 

# Define amenity types of interest
AMENITY_TYPES = ['bakery','bar','cafe','grocery_or_supermarket',
      'movie_theater','park','pharmacy','restaurant','school',
      'spa','subway_station']


def google_places_parser(sess,resp):
  
  if resp.json()['status'] != "OK":
    print resp.url
  
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

  resp.data = (resp.json().get('next_page_token',''), summary)


def make_urls(google_api_key,lat_lng, npt_series):
  ''' Generate query URLs from a series of next-page tokens
  and distinct amenity types '''

  base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
  s = Session()

  urls = []
  for amen, npt in npt_series.iteritems():
    if npt == '':
      search_payload = {"key":google_api_key,
                        "radius":1000,
                        "types":amen,
                        "location":lat_lng}
    else:
      '''Including a page token forces Google to ignore all other
      search parameters'''
      search_payload = {"key":google_api_key,
                        'pagetoken':npt}

    req = Request('GET', base_url, params=search_payload)

    urls.append(s.prepare_request(req).url)

  return urls


def summarizer(x):
  '''x is a Summary namedtuple'''
  nr = np.float64(x.count_rating)
  mu_r = x.sum_rating/nr
  sd_r = np.sqrt(x.sum_rating_sq/nr - mu_r**2)
  npl = np.float64(x.count_price_level)
  mu_p = x.sum_price_level/npl
  sd_p = np.sqrt(x.sum_price_level_sq/npl - mu_p**2)
  
  return (x.count,x.count_rating,mu_r,sd_r,x.count_price_level,mu_p,sd_p) 


def get_local_amenities(google_api_key,lat_lng):
  ''' Given a lat_lng string, return a dataframe contain summary 
  statistics about the amenities within 1 km '''
  session = FuturesSession(max_workers=6)


  amens = AMENITY_TYPES
  amen_dict = dict(zip(amens,
      zip(repeat(''),[Summary(0,0,0,0,0,0,0)]*len(amens))))

  df = pd.DataFrame(amen_dict,index=['npt','summary'])
  get_more = df.loc['npt',:] == ''

  for i in xrange(3):
    urls = make_urls(google_api_key,lat_lng, df.loc['npt',get_more])
    print len(urls)
    results = (session.get(url,background_callback=google_places_parser)
               for url in urls)

    npts, summaries = izip(*(x.result().data for x in results))
    df.loc['npt',get_more] = npts
    df.loc['summary',get_more] = [Summary(*map(operator.add,x[0],x[1]))
        for x in izip(df.loc['summary',get_more],summaries)]

    get_more = df.loc['npt',:] != ''
    if get_more.sum() == 0:
      break
    time.sleep(2) # delay because next page is not immediately available

  df.drop('npt',axis=0,inplace=True)

  # Set the summary columns 
  for amenity in AMENITY_TYPES:
    sum_cols = ['count','count_rating','mean_rating','std_rating',
                'count_price_level','mean_price_level','std_price_level']
    df = pd.concat( [df,pd.DataFrame.from_records(
                        df[amenity].map(lambda x: summarizer(x)).tolist(),
                        columns=[amenity + '_' + s for s in sum_cols],
                        index=df.index)], axis = 1
              )

  return df.drop(AMENITY_TYPES+[col for col in df.columns  
                  if '_count_rating' in col or '_count_price' in col],
                 axis=1)


if __name__ == "__main__":
  lat_lng = '38.939320,-77.059950'
  get_local_amenities(google_api_key,lat_lng)
