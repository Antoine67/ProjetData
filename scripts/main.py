# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:00:48 2020

@author: Antoine
"""

from vrp import VRP
from cvrp import CVRP
from ortools.constraint_solver import routing_enums_pb2
from load_data import from_file_to_adj_matr

#import networkx as nx


import numpy as np
import json 

nb_camions = 5
nb_villes = 17
timeout = 15 # in s

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
    
    matricedemande = [0, 19, 21, 6, 19, 7 ,12,16,6,16,8,14,21,16,3,22,18,19,1,24,8,12,4,8,24,24,2,20,15,2,14,9]
    mat, capacity, cities_nb, vehicules_nb = from_file_to_adj_matr('../data/A-VRP/A-n32-k5.vrp')
    
    # VRP
    #vrp = VRP(vehicules_nb,cities_nb)
    #vrp.create_data_model()
    
    #vrp.pass_matrix(mat)
    #print(vrp.data)
    
    # CVRP
    # TODO
    cvrp = CVRP(vehicules_nb,cities_nb)
    #cvrp.create_data_model()
    cvrp.pass_matrix(mat, matricedemande,capacity)
    print(cvrp.data)
    
    # Display graph
    #G = nx.from_numpy_matrix(vrp.data['distance_matrix']) 
    #nx.draw(G, with_labels=True)
    
    for strategy in algos:
        #solution = vrp.solve(strategy, timeout)
        solution = cvrp.solve(strategy, timeout)
        print(solution)
    

if __name__ == '__main__':
    main()
