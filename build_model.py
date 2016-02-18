import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import dill as pickle

class ColumnSelectTransformer(BaseEstimator, TransformerMixin):
  """
  Select columns of data from nd array
  """
  def __init__(self, columns, rescale=None):
    ''' columns must be list of strings '''
    self.columns = columns
    if rescale == "standard" or rescale=="range" or rescale==None:
      self.rescale = rescale
    else:
      raise NameError("rescale option must specify 'standard' or 'range'")

  def fit(self, X, y):
    return self

  def transform(self, X):
    ''' Assume X is pandas dataframe '''
    df = X[self.columns]
    if self.rescale == "standard":
      return (df-df.mean())/df.std()
    elif self.rescale == "range":
      return (df-df.min())/(df.max()-df.min())
    else:
      return df

if __name__ == "__main__":


  df = pd.read_csv('./data/df_features.csv')
  print df.columns
  '''
  count_cols = [c for c in df.columns 
    if '_count' in c and '_count_' not in c]
  rating_cols = [c for c in df.columns if '_mean_rating' in c]
  price_cols = [c for c in df.columns if '_mean_price' in c]
  '''
  lat_lng_cols = ['latitude','longitude']
  
  clf = Pipeline([
      ('sel',
        ColumnSelectTransformer(lat_lng_cols,rescale=None)),
      ('knn',neighbors.KNeighborsRegressor(n_neighbors=2))
    ])

  X = df[lat_lng_cols]
  X = X.sample(1000)
  y = df.loc[X.index,'SALEPRICE']

  clf.fit(X,y)
  print np.mean(np.abs(clf.predict(X)-y))

  with open('./data/p_combo_model_rf.dpkl','wb') as p_output:
    pickle.dump(clf,p_output)
