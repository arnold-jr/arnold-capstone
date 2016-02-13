from flask import Flask, render_template, request, redirect, g
import os
import sqlite3
from bokeh.resources import CDN 
from bokeh.util.string import encode_utf8
from bokeh_maker import make_plot


app = Flask(__name__)
app.config.from_object('amenidc_settings.Config')
app.config.from_object(os.environ['AMENIDC_SETTINGS'])
print os.environ['AMENIDC_SETTINGS']


'''
DATABASE = './data/sample.db'

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = connect_to_database()
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()
'''


app.vars = {'bokeh_zipcode':'CPBABY',
    'bokeh_script':'',
    'bokeh_div':''}

flag,script,div = make_plot()
if flag:
  app.vars['bokeh_script'] = script
  app.vars['bokeh_div'] = div

@app.route('/')
def main():
  return redirect('/index')


@app.route('/index')
def index():
  js_resources = CDN.render_js()
  css_resources = CDN.render_css()

  html =  render_template(
      'index.html',
      js_resources=js_resources,
      css_resources=css_resources,
      bokeh_script=app.vars['bokeh_script'],
      bokeh_div=app.vars['bokeh_div'],
      bokeh_zipcode=app.vars['bokeh_zipcode'],
      )
  return encode_utf8(html)


@app.route('/about')
def about():

  img_list = [
             ("images/bakery_count.png",
             "images/bakery_mean_rating.png"),
             ("images/bar_count.png",
             "images/bar_mean_rating.png"),
             ("images/cafe_count.png",
             "images/cafe_mean_rating.png"),
             ("images/grocery_or_supermarket_count.png",
             "images/grocery_or_supermarket_mean_rating.png"),
             ("images/movie_theater_count.png",
             "images/movie_theater_mean_rating.png"),
             ("images/park_count.png",
             "images/park_mean_rating.png"),
             ("images/pharmacy_count.png",
             "images/pharmacy_mean_rating.png"),
             ("images/restaurant_count.png",
             "images/restaurant_mean_rating.png"),
             ("images/school_count.png",
             "images/school_mean_rating.png"),
             ("images/spa_count.png",
             "images/spa_mean_rating.png"),
             ("images/subway_station_count.png",
             "images/subway_station_mean_rating.png"),
             ]
  
  return render_template('about.html',img_list=img_list)


if __name__ == '__main__':
  app.run()
