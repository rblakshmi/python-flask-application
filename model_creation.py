# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 18:50:01 2016

@author: lakshmi1
"""

import pandas as pd
import numpy as np
from sklearn import tree as t
from sklearn import ensemble as e
b_data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data" , names = ['id','clump_thickness' , 'size_uniformity ' , 'shape_uniformity' , 'marginal_adhesion' ,'epithelial_size' ,'bare_nuclei' ,'bland cromatin' , 'normal_nuclei' , 'mitosis' , 'class' ] , header = None)
print(b_data.head())
print(b_data.describe())
#finding string values
new_list = list(b_data.select_dtypes(include=[np.object]).columns.values)
print("string value column are")
print(new_list)
#converting string to integer
b_data.bare_nuclei=pd.to_numeric(b_data['bare_nuclei'], errors='coerce')
print(b_data.bare_nuclei.describe())
# finding missing values
print(b_data.bare_nuclei[b_data['bare_nuclei'].isnull()])
#replace missing values
train_m = b_data[['id','clump_thickness','shape_uniformity','marginal_adhesion','epithelial_size','bland cromatin','normal_nuclei','mitosis','class']][b_data['bare_nuclei'].notnull()].values
target_m = b_data['bare_nuclei'][b_data['bare_nuclei'].notnull()].values
test_m = b_data[['id','clump_thickness','shape_uniformity','marginal_adhesion','epithelial_size','bland cromatin','normal_nuclei','mitosis','class']][b_data['bare_nuclei'].isnull()].values
#model creation
model_m=t.DecisionTreeClassifier()
model_final = e.RandomForestClassifier()
#model fit
model_m.fit(train_m , target_m)
print(model_m.score(train_m , target_m))

#replace missing values
b_data.bare_nuclei[b_data['bare_nuclei'].isnull()]= model_m.predict(test_m)
print(b_data.bare_nuclei.describe())
##
###
##

#createfrom sklearn.model_selection import train_test_split
df = pd.DataFrame(np.random.randn(699, 2))
msk = np.random.rand(len(df)) < 0.8
train = b_data[msk]
test = b_data[~msk]

#creating i/p for model
train_final = train[['clump_thickness' , 'size_uniformity ' , 'shape_uniformity' , 'marginal_adhesion' ,'epithelial_size' ,'bare_nuclei' ,'bland cromatin' , 'normal_nuclei' , 'mitosis']].values
target_final = train['class'].values
#model fit
model_final.fit(train_final , target_final)
print(model_final.score)
