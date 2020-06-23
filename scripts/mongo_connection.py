# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 11:16:24 2020

@author: leodi
"""

#Import pymongo to connect to database
from pymongo import MongoClient

#Localhost
client = MongoClient('localhost', 27017)

#Get database and vehicules collection
db = client["DataProject"]
resolved_instances = db["resolved_instances"]

#Only take a few result
results = resolved_instances.find().limit(5)

#Display the result:
for v in results:
  print(v) 

