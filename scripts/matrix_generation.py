from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import random
from model import get_prediction


"""Random adjacency matrix of given size"""
def random_adjacency_matrix_with_model(length, hour, minute):
    
    tab = np.zeros([length, length], dtype = float)
    for i in range(length):
        for j in range(length):
            if(i==j):
                break
            # Max 500 vertices
            pred = get_prediction((i+j)%500,hour,minute)
            tab[i][j] = pred
            tab[j][i] = pred
            
    #print(tab)
            
""" 

Exemple :
random_adjacency_matrix_with_model(500,7,20)

"""