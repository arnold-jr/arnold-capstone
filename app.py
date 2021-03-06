# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, g, jsonify
import os
from wtforms import Form, TextField, validators
import requests
import simplejson as json
import numpy as np
import pandas as pd
import dill as pickle

from geocode_query import get_zip_and_lat_lng
from place_query import get_local_amenities


# Read in app configuration using environment variables
app = Flask(__name__)
app.config.from_object('amenidc_settings.Config')
app.config.from_object(os.environ['AMENIDC_SETTINGS'])
print os.environ['AMENIDC_SETTINGS']

# Define dict for outputting names

DISPLAY_NAMES = {
    "SALEPRICE" : "last sale price",
    "bakery" : "bakeries",
    "bar" : "bars",
    "cafe" : "cafes",
    "grocery_or_supermarket" : "grocery stores",
    "movie_theater" : "movie theaters",
    "park" : "parks",
    "pharmacy" : "pharmacies",
    "restaurant" : "restaurants",
    "school" : "schools",
    "spa" : "spas",
    "subway_station" : "metro stations"
    }

# Read in dataframe and store as app member 
app.vars = {'df':None, 'this_df':None, 'model':None}

try:
  app.vars['df'] = pd.read_csv('./data/df_features.csv')
except:
  print "Database read unsuccessfully"
  pass

if False:
  # Read in pickled sklearn model and store as app member 
  def model_reader():
    with open('./data/p_combo_model_rf.dpkl', 'rb') as p_input:
      model = pickle.load(p_input)
    app.vars['model'] = model

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
  zipcode = int(zipcode)

  df = app.vars['df']
  if zipcode not in df.zipcode.unique():
    this_df = df.mean().to_frame("Mean").transpose()
  else:
    # Model doesn't want to cooperate on heroku
    #query_df = get_local_amenities(google_api_key,lat_lng) 
    #query_df.index = [address[:10]]
    #query_df.loc[address[:10],'SALEPRICE'] = app.vars['model'].predict(
    #    query_df) 
    lat, lng = (float(s) for s in lat_lng.split(","))

    # Use nearest neighbor as prediction
    idx_min = (np.square(df['longitude'].astype(np.float64) - lng)
        +np.square(df['latitude'].astype(np.float64) - lat)).idxmin()
    # Ensure that we only get one row of the dataframe
    query_df = df.loc[[idx_min],:].mean().to_frame(address[:10]).transpose()
    
    # combine zip and query dataframes
    this_df = (df.groupby('zipcode').mean().loc[zipcode,:].to_frame()
        .transpose())
    this_df = query_df.append(this_df)
  
  app.vars['this_df'] = this_df.fillna(0)
  return address, zipcode


def request_cartodb():
  with requests.Session() as s:
    r = s.get(cartodb_api_key)
  return r.json() 


@app.route('/_run_address')
def run_address():
  '''Prepares the data to plot by querying the database and returns JSON
  to the d3 javascript'''
  
  df = app.vars['df'].copy()
  df['SALEPRICE'] = df['SALEPRICE']/100000.0

  
  q_address = request.args.get('a', 'No Address Specified', type=str)
  
  # geocode the address and convert to lat_lng 
  lat_lng, zipcode, address = get_zip_and_lat_lng(
      google_geocode_api_key,q_address)
  zipcode = int(zipcode)
  
  if zipcode not in df.zipcode.unique():
    return jsonify(result=address,
        result_df=[],
        result_saleprice=[])
  
  lat, lng = (float(s) for s in lat_lng.split(","))

  # Use nearest neighbor as prediction
  idx_min = (np.square(df['longitude'].astype(np.float64) - lng)
      +np.square(df['latitude'].astype(np.float64) - lat)).idxmin()
  # Ensure that we only get one row of the dataframe
  query_df = df.loc[[idx_min],:].mean().to_frame(address[:10]).transpose()
  
  # combine zip and query dataframes
  this_df = (df.groupby('zipcode').mean().loc[zipcode,:].to_frame()
      .transpose())
  this_df = query_df.append(this_df)

  this_df = this_df.loc[:,['SALEPRICE']+
      [c for c in this_df.columns.tolist() if ("_count" in c)]]

  zip_samples = df.loc[df.zipcode==zipcode,:].copy()
  ranges = [zip_samples.SALEPRICE.min(), zip_samples.SALEPRICE.mean(), 
    zip_samples.SALEPRICE.max()]
  saleprice_json = {
    "title":"Last sale price / $100k",      
    "subtitle":"",    
    "ranges":ranges,  
    "measures":[this_df.SALEPRICE[0]]
  }
  this_df.drop('SALEPRICE',axis=1,inplace=True)
  chart_data_json = []
  for i,row in this_df.iterrows():  
    val_list = [
        {'label':DISPLAY_NAMES[k.replace("_count","")], 'value':v} 
        for k,v in row.iteritems()]
    chart_data_json.append({'key': i, 'values': val_list}) 

  return jsonify(result=address,
      result_df=chart_data_json,
      result_saleprice=saleprice_json)


@app.route('/', methods=['POST', 'GET'])
def index():
  cartodb_map = request_cartodb()
  map_layers = [
      ("0","mean sale price"),
      ("1","grocery stores"),
      ("2","restaurants"),
      ("3","metro stations"),
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
