# -*- coding: utf-8 -*-
"""
This module contains general supporting functions.

Created on Tue Dec 29 16:31:20 2020
@author: Marijke Thijssen
"""
# %%   Import packages
from functools import wraps
import time


# %%   Functions
def timer(f):
    """ Decorator for timing functions. """
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print('function:%r took: %2.2f sec' % (f.__name__, end - start))
        return result
    
    return wrapper