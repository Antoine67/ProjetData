# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:46:41 2020

@author: Antoine
"""
# Import the necessary packages
from consolemenu import *
from consolemenu.items import *

import os, sys
from ortools.constraint_solver import routing_enums_pb2
from load_data import from_file_to_adj_matr
from load_data import get_particular_info
from mongo_connection import *
from stats import *


from vrp import VRP
from cvrp import CVRP



#import networkx as nx

import time
import numpy as np
import json 
import matplotlib.pyplot as plt

from tqdm import tqdm

import os
import sys

algos_metaheuristic = [
   routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
   routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
]

def displayMenu():
    # Create the menu
    menu = ConsoleMenu("Menu principal", "Projet Data - DIDIER PIQUE EKOBE MOHR HAAS",
                       exit_option_text = "Quitter",
                       )
    vrp_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE EKOBE MOHR HAAS")
    vrp_menu.append_item(FunctionItem("Résoudre un problème VRP", vrp))
    vrp_menu.append_item(FunctionItem("Résoudre un problème CVRP", cvrp))
    
    
    statistics_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE EKOBE MOHR HAAS")

    statistics_executions_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR")
    statistics_executions_menu.append_item(FunctionItem("Execution(s) / Solutions max", call_stats, ["TIMESOLUTIONS"]))
    statistics_executions_menu.append_item(FunctionItem("Execution(s) / Nb vehicules", call_stats, ["TIMEVEHICULES"]))
    statistics_executions_menu.append_item(FunctionItem("Execution(s) / Nb villes", call_stats, ["TIMECITIES"]))

    statistics_display_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR")
    statistics_display_menu.append_item(FunctionItem("Afficher des graphique", call_display_stats, ["TIMESOLUTIONS"]))
   

    

    execution_item = SubmenuItem("Execution", statistics_executions_menu, menu)
    display_item = SubmenuItem("Affichage", statistics_display_menu, menu)
    
    statistics_menu.append_item(execution_item)
    statistics_menu.append_item(display_item)

    vrp_item = SubmenuItem("Solveur (C)VRP", vrp_menu, menu)
    stats_item = SubmenuItem("Statistiques", statistics_menu, menu)

    menu.append_item(vrp_item)
    menu.append_item(stats_item)
    
    # Finally, we call show to show the menu and allow the user to interact
    menu.show()


def vrp():
    mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords = get_mat()
    
    #VRP
    vrp = VRP(vehicules_nb,cities_nb)
    if mat is None:
        vrp.create_data_model()
    else:
        vrp.pass_matrix(mat)
    print(vrp.data)
    vrp_solve(vrp)

def cvrp():   
    mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords = get_mat()
        
    # CVRP
    vrp = CVRP(vehicules_nb,cities_nb)
    if mat is None:
        vrp.create_data_model()
    else:
        vrp.pass_matrix(mat, demand_matrix,capacity)
    print(vrp.data)
    vrp_solve(vrp)

def get_mat():
    random = query_yes_no('Matrice aléatoire ?')
    if(random == True):
        print('Nombre de véhicules ?')
        vehicules_nb = input()
        print('Nombre de villes ?')
        cities_nb = input()
        return None, None, int(cities_nb), int(vehicules_nb), None, None
    
    print('Chemin vers le fichier : ', end='')
    path = input()
    if(os.path.isfile(path) == False):
        raise Exception("Chemin invalide")
    
    mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords = from_file_to_adj_matr(path)
    return mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords
    

def vrp_solve(vrp):

    tabu   = query_yes_no("Utiliser la méthode du Tabou ?")
    sim_an = query_yes_no("Utiliser la méthode du Recuit simulé ?")
    
    algos=[]
    if(tabu):
        algos.append(routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
    if(sim_an):
        algos.append(routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
        

    timeout = 15
    for strategy in algos:
            solution = vrp.solve(strategy, timeout, useTimeout=True)
            print("Solution obtenue : " + str(solution[1]))
            print(solution)

       
    print('Appuyez sur entrée pour continuer...')
    input()
    
    

def call_stats(arg1):
    
    
    print('VRP ou CVRP : ', end='')
    vrp_type = input()
        
    if vrp_type.upper() != 'VRP' and vrp_type.upper() != 'CVRP':
       raise Exception("Type de VRP non reconnu")
       
    dataset_name = None    
    random = query_yes_no("Générer une matrice aléatoirement ?")
    if not random:
        print('Chemin vers le fichier : ', end='')
        path = input()
        
        if(os.path.isfile(path) == False):
            raise Exception("Chemin invalide")
            
        
        dataset_name = os.path.basename(path)    
        mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords = from_file_to_adj_matr(path)
    else:
        print('Entrez le nombre de villes : ', end='')
        cities_nb = int(input())
        print('Entrez le nombre de véhicules : ', end='')
        vehicules_nb = int(input())
        
        dataset_name = "random-k" + str(vehicules_nb) + "-n" + str(cities_nb)

    if vrp_type.upper() == 'VRP':
        # VRP
        vrp = VRP(vehicules_nb,cities_nb)
        if random:
            vrp.create_data_model()
        else:
            vrp.pass_matrix(mat)
        
        
    elif vrp_type.upper() == 'CVRP':
        # CVRP
        vrp = CVRP(vehicules_nb,cities_nb)
        if random:
            vrp.create_data_model()
        else:
            vrp.pass_matrix(mat, demand_matrix,capacity)
    

    
    if arg1.upper()== "TIMESOLUTIONS":
        solutionsLimitArray = []
        while True:
            print('Appuyez sur enter pour arreter l ajout de solution... ')
            print('Entrez un nombre dans le tableau de solutions locales max : ', end='')
            tempLimit = input()
            if tempLimit.isnumeric():
                solutionsLimitArray.append(int(tempLimit))
            else:
                print("Fin de l'entrée, tableau : " , solutionsLimitArray)
                break
            
        
        execution_time_solutions(algos_metaheuristic, vrp, solutionsLimitArray, dataset_name)
    elif arg1.upper()== "TIMEVEHICULES":
        for i in tqdm(range(vehicules_nb)):
            execution_time_vehicules(algos_metaheuristic, vrp, i, dataset_name)
    elif arg1.upper()== "TIMECITIES":
        for i in tqdm(range(cities_nb)):
            execution_time_cities(algos_metaheuristic, vrp, i, dataset_name)
    
    print('Appuyez sur entrée pour continuer...')
    input()
        
def call_display_stats(arg1):

    addNewGraph = True
    arrayToDisplay = []
    name = ""
    
    print('Nom des statistiques à afficher : ', end='')
    name = input()


    while addNewGraph:
        print('Spécification : ', end='')
        specification = int(input())

        
        print('Nom du dataset : ', end='')
        dataset_name = input()

        arrayToDisplay.append({'name':name,
                         'specification':specification,
                         'dataset_name':dataset_name})
        
        
        addNewGraph =   query_yes_no("Ajouter un autre graph ?")
        
    display_statistics(arrayToDisplay)


    
    
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
