# coding: utf-8

import requests
import simplejson as json
import pandas as pd
import numpy as np
from bokeh.plotting import figure 
from bokeh.models import Range1d, LinearAxis
from bokeh.embed import components


DISPLAY_COUNT_KEYS = [
  'SALEPRICE',
  'bakery_count',
  'bar_count',
  'cafe_count',
  'grocery_or_supermarket_count',
  'movie_theater_count',
  'park_count',
  'pharmacy_count',
  'restaurant_count',
  'school_count',
  'spa_count',
  'subway_station_count',
  ]

DISPLAY_RATING_KEYS = [
  'SALEPRICE',
  'bakery_mean_rating',
  'bar_mean_rating',
  'cafe_mean_rating',
  'grocery_or_supermarket_mean_rating',
  'movie_theater_mean_rating',
  'park_mean_rating',
  'pharmacy_mean_rating',
  'restaurant_mean_rating',
  'school_mean_rating',
  'spa_mean_rating',
  'subway_station_mean_rating',
  ]

DISPLAY_PRICE_KEYS = [
  'SALEPRICE',
  'bakery_mean_price_level',
  'bar_mean_price_level',
  'cafe_mean_price_level',
  'grocery_or_supermarket_mean_price_level',
  'movie_theater_mean_price_level',
  'park_mean_price_level',
  'pharmacy_mean_price_level',
  'restaurant_mean_price_level',
  'school_mean_price_level',
  'spa_mean_price_level',
  'subway_station_mean_price_level',
  ]

DISPLAY_VALUES = [
  "Sale price",
  "Bakeries",
  "Bars",
  "Cafes",
  "Groceries",
  "Movie Theaters",
  "Parks",
  "Pharmacies",
  "Restaurants",
  "Schools",
  "Spas",
  "Metro Stations"
  ]


def render_plot(this_df,zipcode,address,amenity_x_type):
  '''Plot the values and return script and div objects'''

  if amenity_x_type == 'count':
    display_keys = DISPLAY_COUNT_KEYS
    xlabel = 'Average Number of Amenities within 1km Radius'
    x_range = Range1d(0,60)
  elif amenity_x_type == 'rating':
    display_keys = DISPLAY_RATING_KEYS
    xlabel = 'Average Star Rating of Amenities within 1km Radius'
    x_range = Range1d(0,5)
  elif amenity_x_type == 'price':
    display_keys = DISPLAY_PRICE_KEYS
    xlabel = 'Average Price Level of Amenities within 1km Radius'
    x_range = Range1d(0,5)

  df = this_df.loc[:,display_keys]
  tools="crosshair,pan,box_zoom,reset,box_select,lasso_select"

  p1 = figure(width=720, height=720,tools=tools, 
        y_range=list(reversed(DISPLAY_VALUES))
      )


  # Set y axis properties
  #p1.yaxis.axis_label = 'Amenity type'
  p1.yaxis.axis_label_text_font_size = '12pt'
  p1.yaxis.major_label_text_font_size = '12pt'
  p1.yaxis.bounds = [-1,len(DISPLAY_VALUES)]

  # Set primary x axis properties
  p1.xaxis.axis_label = xlabel 
  p1.xaxis.axis_label_text_font_size = '12pt'
  p1.xaxis.major_label_text_font_size = '12pt'
  p1.x_range = x_range 

  # Setting the second x axis range name and range
  p1.extra_x_ranges ={"saleprice": Range1d(start=0, end=10)}

  # Adding the second axis to the plot.  
  p1.add_layout(
      LinearAxis(x_range_name="saleprice",
          axis_label='Sale price / $100,000',
          axis_label_text_font_size = '12pt'), 'above')
                    
                    
  # Make background and grid look like seaborn
  p1.background_fill_color = "#EAEAF2"
  p1.grid.grid_line_alpha = 1.0
  p1.grid.grid_line_color = "white"

  #p1.title = title 
  

  height = 0.4
  offsets = np.linspace(-0.5,0.5,2)*height
  colors = [(76,114,176),(253,141,60)]
  legend_items = (address,zipcode)
  j = len(df.columns)
  for k,v in df.iteritems():
    #print k,v.tolist()
    if k == 'SALEPRICE':
      x_range_name = 'saleprice'
      v /= 100000
    else:
      x_range_name = None
    for i in xrange(0,2):
      if j == 1:
        legend_item = legend_items[i]
      else:
        legend_item = None
      
      if j == len(df.columns):
        alpha = 0.7
      else:
        alpha = 1.0

      p1.rect(x=v[i]/2, y=j+offsets[i], width=abs(v[i]), 
          height=height, color=colors[i], fill_alpha=alpha,
          width_units="data", height_units="data",x_range_name=x_range_name,
          legend=legend_item)
    j -= 1
  
  p1.legend.orientation = "bottom_right"
    
  # show the results
  return components(p1)

def make_plots(this_df,zipcode,q_address,amenity_x_type):
  if 1:
    flag = True
    script, div = render_plot(this_df,zipcode,q_address,amenity_x_type)

  else:
    flag, script, div = False, 'Invalid script', 'Invalid div'
   
  return flag, script, div


if __name__ == "__main__":
  make_plots("3801 Connecticut_Ave NW, Washington DC")

