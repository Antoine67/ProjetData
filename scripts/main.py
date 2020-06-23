# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:00:48 2020

@author: Antoine
"""

from vrp import VRP
from cvrp import CVRP
from ortools.constraint_solver import routing_enums_pb2
from load_data import  from_file_to_adj_matr

import networkx as nx


import numpy as np
import json 

nb_camions = 10
nb_villes = 50
timeout = 20 # in s


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
    # VRP
    vrp = VRP(nb_camions,nb_villes)
    #vrp.create_data_model()
    vrp.pass_matrix(from_file_to_adj_matr('../data/A-VRP/A-n32-k5.vrp'))
    print(vrp.data)
    print(len(vrp.data['distance_matrix']))
    
    # CVRP
    # TODO
    #cvrp = CVRP(nb_camions,nb_villes)
    #cvrp.create_data_model()
    
    
    # Display graph
    #G = nx.from_numpy_matrix(vrp.data['distance_matrix']) 
    #nx.draw(G, with_labels=True)
    
    for strategy in algos:
        solution = vrp.solve(strategy, timeout)
        #solution = cvrp.solve(strategy, timeout)
        print(solution)
    

if __name__ == '__main__':
    main()
