import pandas as pd
from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pylab as plt
from scipy.spatial import ConvexHull
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def get_labels(X,n_clusters=11):
  ''' Gets cluster labels for data in x
  
  Args:
    X: numpy array-like of feature vectors
    n_clusters: number of clusters  
  Returns:
    Array of labels
  '''

  if True:
    km = KMeans(n_clusters=n_clusters).fit(X)
    return km.labels_
  if False:
    est = AffinityPropagation().fit(StandardScaler().fit_transform(X))
    return est.labels_
  if False:
    est = DBSCAN(eps=0.1,metric='euclidean').fit( 
        StandardScaler().fit_transform(X) )
    return est.labels_


def create_convex_regions(df_old,xlab='lng',ylab='lat', n_clusters=11):
  ''' Creates convex hulls around subclasses (regions) within a set of points.

  Args:
    df: a mutable pandas dataframe
    xlab: column label of x coordinates
    ylab: column label of y coordinates

  Returns:
    polygons: list of shapely polygons  
  '''
  df = df_old.copy()
 
  Xlabs = (xlab, ylab)  
  new_label = 'kmeans_spatial_label'
  df[new_label] = get_labels(df[[xlab,ylab]],n_clusters)

  fig,ax = plt.subplots(1,1)
  df.plot(kind='scatter', x='lng', y='lat', s=5, c=df[new_label],
      ax=ax,
      colormap=plt.cm.Spectral_r)

  polygons = []
  print(df.columns)
  for i in df[new_label].unique():
    points = df.loc[df[new_label]==i,Xlabs].as_matrix()
    hull = ConvexHull(points)
    for simplex in hull.simplices:
      ax.plot(points[simplex, 0], points[simplex, 1], 'k-')

    # make polygon mask
    polygons.append(Polygon(points[hull.vertices]))
  
  return polygons
