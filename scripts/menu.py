# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:46:41 2020

@author: Antoine
"""
# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
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

from tqdm import tqdm

import os
import sys

algos_metaheuristic = [
   routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
   routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
]

def displayMenu():
    # Create the menu
    menu = ConsoleMenu("Menu principal", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR",
                       exit_option_text = "Quitter",
                       )
    vrp_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR", prologue_text ="Retour au")
    vrp_menu.append_item(FunctionItem("Résoudre un problème (C)VRP à partir d'instances connues", input, ["Enter an input"]))
    vrp_menu.append_item(FunctionItem("Résoudre un problème (C)VRP à partir d'instances aléatoires", input, ["Enter an input"]))
    
    
    statistics_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR")

    statistics_executions_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR")
    statistics_executions_menu.append_item(FunctionItem("Execution(s) / Solutions max", call_stats, ["TIMESOLUTIONS"]))
    statistics_executions_menu.append_item(FunctionItem("Execution(s) / Nb vehicules", call_stats, ["TIMEVEHICULES"]))
    statistics_executions_menu.append_item(FunctionItem("Execution(s) / Nb villes", call_stats, ["TIMECITIES"]))

    statistics_display_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR")

   

    

    execution_item = SubmenuItem("Execution", statistics_executions_menu, menu)
    display_item = SubmenuItem("Affichage", statistics_display_menu, menu)
    statistics_menu.append_item(execution_item)
    statistics_menu.append_item(display_item)

    vrp_item = SubmenuItem("Solveur (C)VRP", vrp_menu, menu)
    stats_item = SubmenuItem("Statistiques", statistics_menu, menu)
    #menu.append_item(function_item)
    menu.append_item(vrp_item)
    menu.append_item(stats_item)
    
    # Finally, we call show to show the menu and allow the user to interact
    menu.show()

def call_stats(arg1):
    
    
    print('VRP ou CVRP : ', end='')
    vrp_type = input()
        
    if vrp_type.upper() != 'VRP' and vrp_type.upper() != 'CVRP':
        print("Type de VRP non reconnu")
        
    random = query_yes_no("Générer une matrice aléatoirement ?")
    if not random:
        print('Chemin vers le fichier : ', end='')
        path = input()
        
        if(os.path.isfile(path) == False):
            print("Chemin invalide")
            return
        
            
        mat, capacity, cities_nb, vehicules_nb, demand_matrix, coords = from_file_to_adj_matr(path)
    else:
        print('Entrez le nombre de villes : ', end='')
        cities_nb = int(input())
        print('Entrez le nombre de véhicules : ', end='')
        vehicules_nb = int(input())

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
            print('appuyez sur enter pour arreter l ajout de solution... ')
            print('Ajouter un nombre de solution limite : ', end='')
            tempLimit = input()
            if tempLimit.isnumeric():
                solutionsLimitArray.append(int(tempLimit))
            else:
                print("Fin de l'entrée des solutions limites")
                print(solutionsLimitArray)
                break
            
        
        execution_time_solutions(algos_metaheuristic, vrp, solutionsLimitArray)
    elif arg1.upper()== "TIMEVEHICULES":
        for i in tqdm(range(vehicules_nb)):
            execution_time_vehicules(algos_metaheuristic, vrp, i)
    elif arg1.upper()== "TIMECITIES":
        for i in tqdm(range(cities_nb)):
            execution_time_cities(algos_metaheuristic, vrp, i)
    
    
        
    
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
