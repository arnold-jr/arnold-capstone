import os
import pandas as pd
from globals import AMENITY_TYPES
from utils import stopwatch

def cat_dbs():
  """ Concatenates databases defined as csv files
  Args:
    None
  Returns:
    df: the concatenated pandas dataframe
  """

  path_template = 'DATA/amenity_db_{0}.csv'

  df = pd.DataFrame()

  for amenity in AMENITY_TYPES: 
    path = path_template.format(amenity)
    if not os.path.isfile(path):
      print(path)
      continue
    
    with stopwatch('appending {0} to database'.format(path)):
      df = df.append(pd.read_csv(path), ignore_index=False)

  df.drop(u'Unnamed: 0',inplace=True, axis=1)

  return df

def store_db(df):
  """ Stores the dataframe as HDF5

  Args:
    df: a pandas dataframe

  Returns:
    None

  """
  
  df.to_hdf('DATA/amenity_db.h5','df')


def merge_all_dbs():
  store_db(cat_dbs())


if __name__ == "__main__":
  print(type(merge_all_dbs()))

