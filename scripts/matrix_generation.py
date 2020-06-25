# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 21:14:17 2020

@author: leodi
"""

from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import random


"""Connection db"""
client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_average_trafic = db['average_trafics']

"""Random adjacency matrix of given size"""
def random_adjacency_matrix(length, minWeight = 1, maxWeight = 10, time = 0):
    
    tab = []
    

    if 7<=time<=9:
        window="avg_matin"
    elif 17<=time<=19:
        window="avg_soir"
    else:
        window="avg_jour"
    
    for num_arete in range(length):
        arete_trafic = list(db.average_trafics.aggregate([{"$match": { "num_arete" : str(num_arete+1)} } ]))
        trafics_jour = [trafic[window] for trafic in arete_trafic]
        
        tab.append(int(random.uniform(int(trafics_jour[0])-(int(trafics_jour[0])*0.1),int(trafics_jour[0])+(int(trafics_jour[0])*0.1))))
    
    tab2d = np.array(tab)
    b = tab2d.transpose().copy()
    b.resize((23,23), refcheck=False)
    b = tab2d.transpose()
    print(b[0])
        

    

random_adjacency_matrix(500,1,5,17)