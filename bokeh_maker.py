# coding: utf-8

import requests
import simplejson as json
import pandas as pd
import numpy as np
from bokeh.plotting import figure 
from bokeh.models import Range1d, LinearAxis
from bokeh.embed import components

DISPLAY_NAMES = {
  'SALEPRICE': "Sale price",
  'bakery_count': "Bakeries",
  'bar_count': "Bars",
  'cafe_count': "Cafes",
  'grocery_or_supermarket_count': "Groceries",
  'movie_theater_count': "Movie Theaters",
  'park_count': "Parks",
  'pharmacy_count': "Pharmacies",
  'restaurant_count': "Restaurants",
  'school_count': "Schools",
  'spa_count': "Spas",
  'subway_station_count': "Metro Stations"
  }

def parse_column_name():
  '''Prepare the data to plot from the database'''
  this_df = pd.DataFrame( 
    {'SALEPRICE': {'20008': 901813.09850746265},
    'bakery_count': {'20008': 6.2850746268656712},
    'bar_count': {'20008': 25.435820895522387},
    'cafe_count': {'20008': 13.088059701492538},
    'grocery_or_supermarket_count': {'20008': 8.7253731343283576},
    'movie_theater_count': {'20008': 1.1417910447761195},
    'park_count': {'20008': 8.4074626865671647},
    'pharmacy_count': {'20008': 8.071641791044776},
    'restaurant_count': {'20008': 43.562686567164178},
    'school_count': {'20008': 18.622388059701493},
    'spa_count': {'20008': 6.4850746268656714},
    'subway_station_count': {'20008': 1.6850746268656716}}
    )

  
  return this_df.append(
    pd.DataFrame.from_dict(
      {'query':
          {'SALEPRICE': 966153.51489868888,
          'bakery_count': 18.389749702026222,
          'bar_count': 56.282479141835516,
          'cafe_count': 41.280691299165674,
          'grocery_or_supermarket_count': 30.650774731823599,
          'movie_theater_count': 1.3510131108462455,
          'park_count': 19.90405244338498,
          'pharmacy_count': 23.856376638855782,
          'restaurant_count': 58.564362336114421,
          'school_count': 45.101907032181167,
          'spa_count': 16.930274135876044,
          'subway_station_count': 2.3134684147794995}
       }, orient='index'
      )
    )

      
def render_plot(this_df):
  '''Plot the values and return script and div objects'''
  # output to static HTML file
  #output_file("lines.html", title="line plot example")
  
  tools="crosshair,pan,box_zoom,reset,box_select,lasso_select"


  p = figure(width=720, height=540,tools=tools, 
      y_range=[ DISPLAY_NAMES[col] 
        for col in reversed(this_df.columns.tolist()) ])

  # Set y axis properties
  p.yaxis.axis_label = 'Amenity type'
  p.yaxis.axis_label_text_font_size = '12pt'
  p.yaxis.major_label_text_font_size = '12pt'

  # Set primary x axis properties
  p.xaxis.axis_label = 'Average Number of Amenities within 1km Radius'
  p.xaxis.axis_label_text_font_size = '12pt'
  p.xaxis.major_label_text_font_size = '12pt'
  p.x_range = Range1d(0,60)

  # Setting the second x axis range name and range
  p.extra_x_ranges ={"saleprice": Range1d(start=0, end=10)}

  # Adding the second axis to the plot.  
  p.add_layout(
      LinearAxis(x_range_name="saleprice",
          axis_label='Sale price / $100,000',
          axis_label_text_font_size = '12pt'), 'above')
                    
                    
  # Make background and grid look like seaborn
  p.background_fill_color = "#EAEAF2"
  p.grid.grid_line_alpha = 1.0
  p.grid.grid_line_color = "white"


  height = 0.4
  offsets = np.linspace(-0.5,0.5,2)*height
  colors = [(76,114,176),(253,141,60)]
  j = len(this_df.columns)
  for k,v in this_df.iteritems():
    #print k,v.tolist()
    if k == 'SALEPRICE':
      x_range_name = 'saleprice'
      v /= 100000
    else:
      x_range_name = None

    for i in xrange(0,2):
      p.rect(x=v[i]/2, y=j+offsets[i], width=abs(v[i]), 
          height=height, color=colors[i],
          width_units="data", height_units="data",x_range_name=x_range_name)
    j -= 1
    
  # show the results
  return components(p)

def make_plot():
  if 1: 
    script, div = render_plot( parse_column_name() )
    return True, script, div
  else:
    return False, 'Invalid script', 'Invalid div'

if __name__ == "__main__":
  make_plot()

