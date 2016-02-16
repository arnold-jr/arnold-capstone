from flask import Flask, render_template, request, redirect, g
from wtforms import Form, TextField, validators
import requests
import simplejson as json
import pandas as pd
import os
import sqlite3
from bokeh.resources import CDN 
from bokeh.util.string import encode_utf8

from geocode_query import get_zip_and_lat_lng
from place_query import get_local_amenities
from bokeh_maker import make_plots


# Read in all API keys
with open("../secrets/amenidc_secrets.json.nogit") as fh: 
  secrets = json.loads(fh.read())
  google_api_key = secrets['google_server_api_key']
  google_geocode_api_key = secrets['google_geocode_api_key']
  cartodb_api_key = secrets['cartodb_api_key']

app = Flask(__name__)
app.config.from_object('amenidc_settings.Config')
app.config.from_object(os.environ['AMENIDC_SETTINGS'])
print os.environ['AMENIDC_SETTINGS']

app.vars = {'df':None, 'this_df':None}
def data_reader():
  #global app
  df = pd.read_csv('./data/mean_by_zip_04.csv')
  df['zipcode'] = df['zipcode'].astype(str)
  df.set_index('zipcode',inplace=True)
  app.vars['df'] = df 

data_reader()

def prep_plot_df(q_address):
  '''Prepare the data to plot by a) quering the mean_by_zipcode database
  and b) querying nearby places using Google places API'''
  # geocode the address and convert to lat_lng 
  lat_lng, zipcode, address = get_zip_and_lat_lng(google_geocode_api_key,q_address)
  print lat_lng, zipcode, address

  this_df = app.vars['df'].loc[[zipcode],:]
  this_df =  this_df.append(get_local_amenities(google_api_key,lat_lng))

  # predict this price
  this_df.loc['summary','SALEPRICE'] = 1000000.0
  
  app.vars['this_df'] = this_df.fillna(0)
  return address, zipcode


@app.route('/')
def main():
  return redirect('/index')

def request_cartodb():
  with requests.Session() as s:
    r = s.get(cartodb_api_key)
  return r.json() 

class AddressQueryForm(Form):
  address = TextField('DC Street Address', 
      [validators.Length(min=6, max=512)])


@app.route('/index', methods=['POST', 'GET'])
def index():
  cartodb_map = request_cartodb()
  
  form = AddressQueryForm(request.form) 

  js_resources = CDN.render_js()
  css_resources = CDN.render_css()

  amenity_x_type, amenity_x_disp = 'price','Average Price Level'

  if request.method == 'POST' and form.validate():
    q_address = form.address.data 
    f_address,zipcode = prep_plot_df(q_address) 
    
    flag, bokeh_script, bokeh_div = make_plots(app.vars['this_df'],
        q_address, zipcode, 'rating')
    bp_visibility="visible"
  elif request.method == 'GET':
    flag, bokeh_script, bokeh_div = (False, '', '')
    bp_visibility="hidden"
  
  html =  render_template(
      'index.html',
      cartodb_map=cartodb_map,
      form=form,
      bp_visibility=bp_visibility,
      amenity_x_disp=amenity_x_disp,
      js_resources=js_resources,
      css_resources=css_resources,
      bokeh_script=bokeh_script,
      bokeh_div=bokeh_div,
      )
  return encode_utf8(html)


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
  ]
  
  return render_template('about.html',img_list=img_list)


if __name__ == '__main__':
  app.run()
