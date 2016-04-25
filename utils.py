from collections import namedtuple
from itertools import izip
import contextlib
import time

SumBase = namedtuple('SumBase', ['count',
  'count_rating','sum_rating','sum_rating_sq',
  'count_price_level','sum_price_level','sum_price_level_sq'])

class SumTuple(SumBase):
  def __init__(self, count, 
      count_rating, sum_rating, sum_rating_sq, 
      count_price_level, sum_price_level,sum_price_level_sq):
    
    self = SumBase(count, 
        count_rating, sum_rating, sum_rating_sq, 
        count_price_level, sum_price_level, sum_price_level_sq)
    
  def __iadd__(self, other):
    if not isinstance(other,SumTuple):
      raise TypeError
    return SumTuple(*(t[0]+t[1] for t in izip(self,other)))


@contextlib.contextmanager
def stopwatch(message):
  """Context manager to print how long a block of code took."""
  t0 = time.time()
  try:
    yield
  finally:
    t1 = time.time()
    print('Total elapsed time for %s: %.3f s' % (message, t1 - t0))
