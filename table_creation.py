# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:44:00 2016

@author: lakshmi1
"""

import sqlite3
import os
conn = sqlite3.connect('librarymanagement.sqlite')
print(" opened successfully")
c = conn.cursor()
c.execute('''CREATE TABLE Book (TITLE text,CATEGORY text,AUTHOR text,DATE text,GENRE text,SYNOPSIS text)''')
print("created successfully")
c.execute("INSERT INTO LOGIN VALUES (,'Rb','nanaganallur',12345,21)")

print("successfully inserted")
conn.commit()
conn.close()
