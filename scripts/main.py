# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:00:48 2020

@author: Antoine
"""

from vrp import VRP
#from cvrp import CVRP
from ortools.constraint_solver import routing_enums_pb2 

import networkx as nx


nb_camions = 3
nb_villes = 50
timeout = 10 # in s

algos = [
   routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
   routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
         ]
def main():
    
    vrp = VRP(nb_camions,nb_villes)
    print(vrp.data)
    
    #Display graph
    G = nx.from_numpy_matrix(vrp.data['distance_matrix']) 
    nx.draw_circular(G, with_labels=True)
        
    for strategy in algos:
        #VRP
       
        solution = vrp.solve(strategy, timeout)
       
        print(solution)
        
        
        
        #CVRP




if __name__ == '__main__':
    main()
