# coding: utf-8

import requests
import string
from datetime import date, timedelta
import simplejson as json
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

def parse_column_name(col):
  '''Prepare the data to plot from the database'''

  x = np.random.rand(100) 
  Y = np.log(x)
  return x, Y

def render_plot(x,Y):
  '''Plot the x and Y values and return script and div objects'''
  # output to static HTML file
  output_file("lines.html", title="line plot example")

  TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset, \
    box_select,lasso_select"

  # create a new plot with a title and axis labels
  p = figure(width=600, height=450, tools=TOOLS)

  #p = figure(width=400, height=300,
  #       title="simple line example", x_axis_type='datetime', 
  #       x_axis_label='x', y_axis_label='y',
  #       tools=TOOLS)


  # add a line renderer with legend and line thickness
  p.line(x, np.log(x), line_width=1, color='gray')


  #p.legend.orientation = "top_left"
  p.grid.grid_line_alpha=0
  p.xaxis.axis_label = 'Date'
  p.xaxis.axis_label_text_font_size = '14pt'
  p.xaxis.major_label_text_font_size = '14pt'

  p.yaxis.major_label_text_font_size = '14pt'
  p.yaxis.axis_label = 'Price / $'

  p.yaxis.axis_label_text_font_size = '14pt'
  p.ygrid.band_fill_color="olive"
  p.ygrid.band_fill_alpha = 0.1

  # show the results
  return components(p)

def make_plot(col):
  x,Y = parse_column_name(col)
  if True:
    script, div = render_plot(x,Y)
    return True, script, div
  else:
    return False, 'Invalid script', 'Invalid div'


