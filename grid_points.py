import numpy as np
from collections import namedtuple
from itertools import repeat

def generate_grid_points(bnd_box=(-77.13,-76.90,38.79,39.),radius=500):
  """ Generates a list of lat/lng coordinates representing vertices
    on a diamond-shaped grid of equilateral triangles 
 
  Args:
    bnd_box: coordinates of bounding box, [x0, x1, y0, y1]
    radius: search radius, in meters

  Returns:
    coords: list of (lng,lat) coordinates of the grid points
  """
  
  

  # define bounding lats and lngs in degrees
  # lat
  y0 = bnd_box[2]
  y1 = bnd_box[3]
  lat_ctr = (y1+y0)/2

  # lng
  x0 = bnd_box[0]
  x1 = bnd_box[1]
  lng_ctr = (x1+x0)/2

  # define radius R in meters
  r = radius 

  hx = np.sqrt(3)/1.1*r

  conversion_lat = 1./111111.
  hy = 2*r/1.1*conversion_lat
  coords = []
  for j in xrange(int(np.ceil((y1-y0)/hy)),-1,-1):
    lat = y0+j*hy
    
    # degrees per meter
    conversion_lng = 1./111111/np.cos(np.deg2rad(lat))
    hx = hx = np.sqrt(3)/1.1*r*conversion_lng
    
    # account for offset of the equilateral triangles
    lng = [(j%2)*hx/2+x0+i*hx for i in xrange(int(np.ceil((x1-x0)/hx)))]
    coords.extend(
        zip(repeat(lat),
          (g for g in lng 
            if np.abs((g-lng_ctr)/(x1-x0))+np.abs((lat-lat_ctr)/(y1-y0)) 
            < 0.6 )))
    
  return coords
