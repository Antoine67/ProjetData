# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:00:48 2020

@author: Antoine
"""

from vrp import VRP
from cvrp import CVRP
from ortools.constraint_solver import routing_enums_pb2
from load_data import from_file_to_adj_matr
from load_data import get_particular_info
from mongo_connection import *
from stats import *

#import networkx as nx

import time
import numpy as np
import json 
import matplotlib.pyplot as plt

nb_camions = 5
nb_villes = 17
timeout = 15 # in s

cvrpOrVrp = 'cvrp'
random = False

"""
AUTOMATIC            	Lets the solver select the metaheuristic.
GREEDY_DESCENT      	  	Accepts improving (cost-reducing) local search neighbors until a local minimum is reached.
GUIDED_LOCAL_SEARCH 	  	Uses guided local search to escape local minima (cf. http://en.wikipedia.org/wiki/Guided_Local_Search); this is generally the most efficient metaheuristic for vehicle routing.
SIMULATED_ANNEALING 	  	Uses simulated annealing to escape local minima (cf. http://en.wikipedia.org/wiki/Simulated_annealing).
TABU_SEARCH         	  	Uses tabu search to escape local minima (cf. http://en.wikipedia.org/wiki/Tabu_search).
OBJECTIVE_TABU_SEARCH   	Uses tabu search on the objective value of solution to escape local minima
"""

algos = [
   routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
   routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
]

def main():
    
    mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords = from_file_to_adj_matr('../data/A-VRP/A-n33-k6.vrp')
    cost = get_particular_info('../data/A-VRP-sol/opt-A-n32-k5', 'cost')
    solutionsLimitArray = [100,200]
    

    if cvrpOrVrp == 'vrp':
        # VRP
        vrp = VRP(vehicules_nb,cities_nb)
        if random:
            vrp.create_data_model()
        else:
            vrp.pass_matrix(mat)
        print(vrp.data)
        
        
    elif cvrpOrVrp == 'cvrp':
        # CVRP
        vrp = CVRP(vehicules_nb,cities_nb)
        if random:
            vrp.create_data_model()
        else:
            vrp.pass_matrix(mat, demand_matrix,capacity)
        print(vrp.data)



    # Résoud le problème du VRP/CVRP
    
    for strategy in algos:
            solution = vrp.solve(strategy, timeout, useTimeout=True, useHeuristic=True)
            if not random:
                print("Solution attendue : " + str(cost))
            print("Solution obtenue : " + str(solution[1]))
            print(solution)
           

    # Créér des stats sur le vrp
    #execution_time_solutions(algos, vrp, solutionsLimitArray)

    """
    # Afficher des statistiques
    display_statistics([{'name':'temps execution en fonction des solutions',
                         'specification':3,
                         'dataset_name':'A-n33-k6'},
                        {'name':'temps execution en fonction des solutions',
                         'specification':4,
                         'dataset_name':'A-n33-k6'}])
    """ 
 
    # Afficher le graphique des villes
    #G = nx.from_numpy_matrix(vrp.data['distance_matrix']) 
    #nx.draw(G, with_labels=True)
    
    

if __name__ == '__main__':
    main()
