# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 19:19:27 2016

@author: lakshmi1
"""

import os
import pickle
dest = os.path.join('breast_cancer', 'pkl_objects')
if not os.path.exists(dest):
    os.makedirs(dest)
pickle.dump(model_final, open(os.path.join(dest , 'model.pkl'), 'wb'))
print("success")