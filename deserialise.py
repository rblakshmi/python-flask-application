# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:23:57 2016

@author: lakshmi1
"""

import pickle
import os
cur_dir = os.path.dirname(__file__)
stop = pickle.load(open(os.path.join(cur_dir,'model.pkl'), 'rb'))
print(stop)