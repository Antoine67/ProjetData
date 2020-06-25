from pymongo import MongoClient
from mongo_connection import *
from ortools.constraint_solver import routing_enums_pb2

import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time
from tqdm import tqdm

SpecDico = {routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING:"Recuit Simulé",
            routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH:"Tabou"}

def display_graph(specifications):


    for spec in specifications:          
        plt.plot(spec['x'], spec['y'], 'o', label=SpecDico[spec['specification']] + " / " + spec['dataset_name'])
    
    
    plt.ylabel(specifications[0]['y_label'])
    plt.xlabel(specifications[0]['x_label'])
    plt.suptitle(specifications[0]['name'])
    
    plt.legend()
    
    plt.show()

def execution_time_solutions(algos, vrp, solutionsLimitArray, dataset_name):

    stats_strategy = []
    stats_x = []
    stats_y = []
    
    for strategy in algos:
        temp_stats_x = []
        temp_stats_y = []
        for solutionLimit in tqdm(solutionsLimitArray, desc = SpecDico[strategy]):
                # Get the time execution for statistics
                start_time = time.time()
                
                solution = vrp.solve(strategy, solutionLimit, False)


                execution_time = time.time() - start_time
                temp_stats_x.append(solutionLimit)
                temp_stats_y.append(execution_time)
        stats_strategy.append(strategy)
        stats_x.append(temp_stats_x)
        stats_y.append(temp_stats_y)
        
    insert_multiple_stats(stats_x, stats_y, 'Temps execution en fonction des solutions', 'Solution', 'Temps (s)', stats_strategy, dataset_name)

def execution_time_vehicules(algos, vrp, vehicules_nb, dataset_name):
    solutionLimit = 100
    stats_strategy = []
    stats_x = []
    stats_y = []
    
    for strategy in algos:
        temp_stats_x = []
        temp_stats_y = []
        
        # Get the time execution for statistics
        start_time = time.time()

        vrp.k = vehicules_nb       
        solution = vrp.solve(strategy, solutionLimit)

        execution_time = time.time() - start_time
        temp_stats_x.append(vehicules_nb)
        temp_stats_y.append(execution_time)
        stats_strategy.append(strategy)
        
        stats_x.append(temp_stats_x)
        stats_y.append(temp_stats_y)
        

    insert_multiple_stats(stats_x, stats_y, 'Temps execution en fonction du nombre de véhicules', 'Nombre de véhicules', 'Temps (s)', stats_strategy, dataset_name)



def execution_time_cities(algos, vrp, cities_nb, dataset_name):
    solutionLimit = 100
    stats_strategy = []
    stats_x = []
    stats_y = []
    
    for strategy in algos:
        temp_stats_x = []
        temp_stats_y = []
        
        # Get the time execution for statistics
        start_time = time.time()

        vrp.towns_nb = cities_nb        
        solution = vrp.solve(strategy, solutionLimit)

        execution_time = time.time() - start_time
        temp_stats_x.append(cities_nb)
        temp_stats_y.append(execution_time)
        stats_strategy.append(strategy)
        
        stats_x.append(temp_stats_x)
        stats_y.append(temp_stats_y)
        

    insert_multiple_stats(stats_x, stats_y, 'Temps execution en fonction du nombre de ville', 'Nombre de ville', 'Temps (s)', stats_strategy, dataset_name)    

def execution_quality_cities(algos, vrp, cities_nb, dataset_name, cost):
    solutionLimit = 100
    stats_strategy = []
    stats_x = []
    stats_y = []
    
    for strategy in algos:
        temp_stats_x = []
        temp_stats_y = []
        
        # Get the time execution for statistics

        vrp.towns_nb = cities_nb        
        solution = vrp.solve(strategy, solutionLimit)


        temp_stats_x.append(cities_nb)
        temp_stats_y.append(abs(solution[1]/cost)) # en pourcentage
        stats_strategy.append(strategy)
        
        stats_x.append(temp_stats_x)
        stats_y.append(temp_stats_y)
        

    insert_multiple_stats(stats_x, stats_y, 'Qualité de la solution en fonction du nombre de ville', 'Nombre de ville', 'Ecart', stats_strategy, dataset_name)

def display_statistics(arrayIN):

    specifications = []
    
    for array in arrayIN:
        specifications.append(get_avg_stats2(array["name"],array["specification"],array["dataset_name"]))
    
    display_graph(specifications)
