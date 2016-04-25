import numpy as np
import matplotlib
import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from collections import namedtuple


def plot_radii():
  """ Plots radii emanating from vertices of an equilateral triangle.
  Demonstrates the optimal radius length of s/sqrt(3) for side length s"""

  codes = [Path.MOVETO,
           Path.LINETO,
           Path.LINETO,
           Path.CLOSEPOLY,
           ]

  Point = namedtuple('Point',['x','y','sign'])

  h = 1.
  R = h/np.sqrt(3)

  ctrs = [Point(0.,0.,-1),Point(h,0.,-1),Point(h/2., -h*np.sqrt(3)/2,1)]

  x = h/2.
  y = [c.y + c.sign*np.sqrt(R**2 - (x-c.x)**2) for c in ctrs]


  # Plot an example image
  xs,ys,_ = zip(*ctrs)
  fig,ax = plt.subplots(1,1)
  ax.set_aspect('equal')
  ax.scatter(xs,ys,color='k')
  path = Path([c[0:2] for c in ctrs]+[ctrs[0][0:2]], codes)
  patch = patches.PathPatch(path, fill=False)
  ax.add_patch(patch)

  for c in ctrs:
    ax.add_artist(plt.Circle(c,1./np.sqrt(3),fill=False, color='r'))
    ax.add_artist(plt.Circle(c,1.05/np.sqrt(3),fill=False, color='b'))

  plt.show()

if __name__ == "__main__":
  plot_radii()
