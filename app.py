from flask import Flask, render_template, request, redirect, g, jsonify
import os

from wtforms import Form, TextField, validators

import requests
import simplejson as json
import pandas as pd

import dill as pickle


from geocode_query import get_zip_and_lat_lng
from place_query import get_local_amenities

# Read in all API keys from environment
google_api_key = os.environ['GOOGLE_SERVER_API_KEY']
google_geocode_api_key = os.environ['GOOGLE_GEOCODE_API_KEY']
cartodb_api_key = os.environ['CARTODB_API_KEY']


# Read in app configuration using environment variables
app = Flask(__name__)
app.config.from_object('amenidc_settings.Config')
app.config.from_object(os.environ['AMENIDC_SETTINGS'])
print os.environ['AMENIDC_SETTINGS']


# Read in dataframe and store as app member 
app.vars = {'df':None, 'this_df':None, 'model':None}
def data_reader():
  df = pd.read_csv('./data/mean_by_zip_04.csv')
  df['zipcode'] = df['zipcode'].astype(str)
  df.set_index('zipcode',inplace=True)
  app.vars['df'] = df 
try:
  data_reader()
except:
  print "Database read unsuccessfully"
  pass

# Read in pickled sklearn model and store as app member 
def model_reader():
  with open('./data/p_combo_model_rf.dpkl', 'rb') as p_input:
    model = pickle.load(p_input)
  app.vars['model'] = model
  #print model.get_params()
try:
  model_reader()
except:
  print "Model read unsuccessfully"
  pass


def prep_plot_df(q_address):
  '''Prepare the data to plot by a) quering the mean_by_zipcode database
  and b) querying nearby places using Google places API'''
  # geocode the address and convert to lat_lng 
  lat_lng, zipcode, address = get_zip_and_lat_lng(
      google_geocode_api_key,q_address)
  print lat_lng, zipcode, address

  address
  if True or zipcode not in df.index:
    this_df = app.vars['df'].mean().to_frame("Mean").transpose()
  else:
    zip_df = app.vars['df'].loc[[zipcode],:]
    #query_df = get_local_amenities(google_api_key,lat_lng) 
    query_df = zip_df

    # predict this price
    #query_df.loc['summary','SALEPRICE'] = 1000000.0
    query_df.loc['summary','SALEPRICE'] = app.vars['model'].predict(query_df) 
    
    # combine zip and query dataframes
    this_df = zip_df.append(query_df)
  
  app.vars['this_df'] = this_df.fillna(0)
  return address, zipcode


def request_cartodb():
  with requests.Session() as s:
    r = s.get(cartodb_api_key)
  return r.json() 


@app.route('/_run_address')
def run_address():
  q_address = request.args.get('a', 'No Address Specified', type=str)

  address, zipcode = prep_plot_df('1129 Maryland Ave') 

  df = app.vars['this_df']
  df = df.loc[:,[c for c in df.columns.tolist() if "_count" in c 
    and "count_" not in c]]

  chart_data_json = []
  for i,row in df.iterrows():  
    val_list = [{'label':k, 'value':v} for k,v 
        in row.to_dict().iteritems()]
    chart_data_json.append({'key': i, 'values': val_list}) 
  
  #chart_data_json = [ { "key": "Zipcode", "values": [ { "label" : "Fish" , "value" : -1.8746444827653 } , { "label" : "Group B" , "value" : -8.0961543492239 } , { "label" : "Group C" , "value" : -0.57072943117674 } , { "label" : "Group D" , "value" : -2.4174010336624 } , { "label" : "Group E" , "value" : -0.72009071426284 } , { "label" : "Group F" , "value" : -2.77154485523777 } , { "label" : "Group G" , "value" : -9.90152097798131 } , { "label" : "Group H" , "value" : 14.91445417330854 } , { "label" : "Group I" , "value" : -3.055746319141851 } ] }, { "key": "Zipcode", "values": [ { "label" : "Fish" , "value" : -1.8746444827653 } , { "label" : "Group B" , "value" : -8.0961543492239 } , { "label" : "Group C" , "value" : -0.57072943117674 } , { "label" : "Group D" , "value" : -2.4174010336624 } , { "label" : "Group E" , "value" : -0.72009071426284 } , { "label" : "Group F" , "value" : -2.77154485523777 } , { "label" : "Group G" , "value" : -9.90152097798131 } , { "label" : "Group H" , "value" : 14.91445417330854 } , { "label" : "Group I" , "value" : -3.055746319141851 } ] }, ]

  print chart_data_json
  return jsonify(result=address,
      result_df=chart_data_json)


@app.route('/', methods=['POST', 'GET'])
def index():
  cartodb_map = request_cartodb()
  map_layers = [
      ("0","Mean Sale Price"),
      ("1","Groceries"),
      ("2","Restaurants"),
      ("3","Metro Stations"),
      ]


  html =  render_template(
      'index.html',
      cartodb_map=cartodb_map,
      map_layers=map_layers,
      )
  return html


@app.route('/about')
def about():

  img_list = [
    ("images/bakery_count.png",
    "images/bakery_mean_price_level.png",
    "images/bakery_mean_rating.png",),
    ("images/bar_count.png",
    "images/bar_mean_price_level.png",
    "images/bar_mean_rating.png",),
    ("images/cafe_count.png",
    "images/cafe_mean_price_level.png",
    "images/cafe_mean_rating.png",),
    ("images/grocery_or_supermarket_count.png",
    "images/grocery_or_supermarket_mean_price_level.png",
    "images/grocery_or_supermarket_mean_rating.png",),
    ("images/movie_theater_count.png",
    "images/movie_theater_mean_price_level.png",
    "images/movie_theater_mean_rating.png",),
    ("images/park_count.png",
    "images/park_mean_price_level.png",
    "images/park_mean_rating.png",),
    ("images/pharmacy_count.png",
    "images/pharmacy_mean_price_level.png",
    "images/pharmacy_mean_rating.png",),
    ("images/restaurant_count.png",
    "images/restaurant_mean_price_level.png",
    "images/restaurant_mean_rating.png",),
    ("images/school_count.png",
    "images/school_mean_price_level.png",
    "images/school_mean_rating.png",),
    ("images/spa_count.png",
    "images/spa_mean_price_level.png",
    "images/spa_mean_rating.png",),
    ("images/subway_station_count.png",
    "images/subway_station_mean_price_level.png",
    "images/subway_station_mean_rating.png",),
  ]
  
  return render_template('about.html',img_list=img_list)


if __name__ == '__main__':
  app.run()
