from flask import Flask, render_template, request, redirect
import os
from bokeh.resources import CDN 
from bokeh.util.string import encode_utf8
from bokeh_maker import make_plot
 
app = Flask(__name__)
app.config.from_object('amenidc_settings.Config')
app.config.from_object(os.environ['AMENIDC_SETTINGS'])
print os.environ['AMENIDC_SETTINGS']


app.vars = {'plot_name':'cmg',
    'bokeh_script':'',
    'bokeh_div':''}

flag,script,div = make_plot(app.vars['plot_name'])
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
      )
  return encode_utf8(html)


if __name__ == '__main__':
  app.run(debug=True)
  #app.run(host='0.0.0.0',debug=False)
