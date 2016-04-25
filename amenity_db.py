import pandas as pd
from globals import AMENITY_TYPES, google_api_key
from grid_points import generate_grid_points
from grid_query import get_local_amenities


def gen_amenity_db():
  """ Creates an amenity database by querying a grid of points and 
  requesting Google Places API within a given radius

  Args:
    none
  Returns:
    none

  """
  radius = 500
  db_name = 'DATA/amenity_db.h5'

  # get the grid coordinates
  lat,lng,lat_lng_strs = generate_grid_points(radius=radius)

  for amenity in AMENITY_TYPES:
  # store the query results in an HDF store 
    with pd.get_store(db_name, mode='w') as store: 
      store.append('df',
          get_local_amenities(google_api_key,
              lat_lng_strs,
              amenity,
              radius=radius)
      print('Appending \'{0}\' search to dataframe'.format(amenity))

if __name__ == "__main__":
  gen_amenity_db()
