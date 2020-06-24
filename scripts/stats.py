from pymongo import MongoClient
from mongo_connection import *

import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time


def display_graph(specifications):

    for spec in specifications:          
        plt.plot(spec['x'], spec['y'], 'o', label=spec['specification'])
    
    
    plt.ylabel(specifications[0]['y_label'])
    plt.xlabel(specifications[0]['x_label'])
    plt.suptitle(specifications[0]['name'])
    
    plt.legend()
    
    plt.show()

def execution_time_solutions(algos, vrp, solutionsLimitArray, useHeuristic):

    stats_strategy = []
    stats_x = []
    stats_y = []
    
    for strategy in algos:
        temp_stats_x = []
        temp_stats_y = []
        for solutionsLimit in solutionsLimitArray:
                # Get the time execution for statistics
                start_time = time.time()
                
                solution = vrp.solve(strategy, solutionsLimit, useTimeout = False, useHeuristic = useHeuristic)

                execution_time = time.time() - start_time
                print(strategy,execution_time)
                temp_stats_x.append(solutionsLimit)
                temp_stats_y.append(execution_time)
                stats_strategy.append(strategy)
        stats_x.append(temp_stats_x)
        stats_y.append(temp_stats_y)
        
    insert_multiple_stats(stats_x, stats_y, "temps execution en fonction des solutions", "Solution","Temps (s)", stats_strategy, 'A-n33-k6')



def display_statistics(arrayIN):

    specifications = []
    
    for array in arrayIN:
        specifications.append(get_avg_stats2(array["name"],array["specification"],array["dataset_name"]))
    
    display_graph(specifications)
