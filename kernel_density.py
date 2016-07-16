import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets.species_distributions import construct_grids
from sklearn.preprocessing import MinMaxScaler, FunctionTransformer
from sklearn.neighbors import KernelDensity
from sklearn import pipeline
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def calc_kernel_density(X,polygons):
  ''' Calculates kernel density and creates a contour plot 

  Args:
    Xtrain: np nd-array like of X data
    polygons: list of shapely polygon objects
  Returns:
    

  '''
  
  k_pipe = pipeline.Pipeline([
    ('scale',MinMaxScaler()),
    ('kde', KernelDensity(bandwidth=0.4, metric='euclidean',
                      kernel='gaussian', algorithm='ball_tree')),
    ])


  k_pipe.fit(X)


  npts = 501
  min_X = X.min(axis=0)
  max_X = X.max(axis=0)
  xgrid = np.linspace(min_X[0],max_X[0],npts)
  ygrid = np.linspace(min_X[1],max_X[1],npts)
  X, Y = np.meshgrid(xgrid,ygrid)
  xy = np.vstack([X.ravel(), Y.ravel()]).T

  land_mask = np.zeros(xy.shape[0],dtype=np.bool)
  for polygon in polygons:
    land_mask = np.logical_or(land_mask, 
        np.array(map(lambda p: polygon.contains(Point(p)),xy)))

  xy = xy[land_mask,:]

  # create response surface 
  Z = np.empty(np.prod(X.shape))
  Z.fill(np.nan)
  Z[land_mask] = k_pipe.named_steps['kde'].score_samples(xy)
  Z = Z.reshape(X.shape)

  # plot contours of the density
  levels = np.linspace(np.nanmin(Z), np.nanmax(Z), 25)
  fig,ax = plt.subplots(1,1)
  ax.contourf(X, Y, Z, levels=levels, cmap=plt.cm.Reds_r)
