import pandas as pd
from globals import AMENITY_TYPES, google_api_key
from grid_points import generate_grid_points
from grid_query import get_local_amenities
from utils import stopwatch

def gen_amenity_db():
  """ Creates an amenity database by querying a grid of points and 
  requesting Google Places API within a given radius

  Args:
    none
  Returns:
    none

  """
  radius = 500
  db_name = 'DATA/amenity_db'

  with stopwatch('generating grid coordinates'):
    # get the grid coordinates
    lat,lng,lat_lng_strs = generate_grid_points(radius=radius)

  for amenity in AMENITY_TYPES:
    if amenity <= 'fire_station':
      continue
    
    with stopwatch('requesting amenties'):
      # get the amenities dataframe
      df = get_local_amenities(google_api_key,
                lat_lng_strs,
                amenity,
                radius=radius)
     
      print(df.columns)
    
    with stopwatch('appending \'{0}\' search to dataframe'.format(amenity)):
      # store the query results in an HDF store 
      #df.to_hdf(db_name,'df',append=True)
      df.to_csv(db_name+'_'+amenity+'.csv') 

if __name__ == "__main__":
  gen_amenity_db()
