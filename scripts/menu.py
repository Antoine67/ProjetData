# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:46:41 2020

@author: Antoine
"""
# Import the necessary packages
from consolemenu import *
from consolemenu.items import *

def displayMenu():
    # Create the menu
    menu = ConsoleMenu("Menu principal", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR",
                       exit_option_text = "Quitter",
                       )
    vrp_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR", prologue_text ="Retour au")
    vrp_menu.append_item(FunctionItem("Résoudre un problème (C)VRP à partir d'instances connues", input, ["Enter an input"]))
    vrp_menu.append_item(FunctionItem("Résoudre un problème (C)VRP à partir d'instances aléatoires", input, ["Enter an input"]))
    
    
    statistics_menu = ConsoleMenu("Sélectionnez une action :", "Projet Data - DIDIER PIQUE HAAS EKOBE MOHR")
    statistics_menu.append_item(FunctionItem("Execution(s) / Solutions max", input, ["Enter an input"]))
    statistics_menu.append_item(FunctionItem("Execution(s) / Nb vehicules", input, ["Enter an input"]))
    statistics_menu.append_item(FunctionItem("Execution(s) / Nb villes", input, ["Enter an input"]))

    vrp_item = SubmenuItem("Solveur (C)VRP", vrp_menu, menu)
    stats_item = SubmenuItem("Statistiques", statistics_menu, menu)
    
    #menu.append_item(function_item)
    menu.append_item(vrp_item)
    menu.append_item(stats_item)
    
    # Finally, we call show to show the menu and allow the user to interact
    menu.show()
