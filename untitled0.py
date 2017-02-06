# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 08:58:48 2016

@author: lakshmi1
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('patient.sqlite')
c = conn.cursor()
username = "harini"
id = "1022"
c.execute('SELECT ID,NAME FROM patient_db')
users = c.fetchall()
data = pd.DataFrame(users , columns = ['id' , 'name'])
data.index = data['name']
print(data)