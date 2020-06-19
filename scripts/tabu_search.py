# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#tabu search

import numpy as np


def recherche_tabou(element_initial, taille_tabou, iter_max):
    """
    1. On part d'un element de notre ensemble de recherche qu'on declare element courant
    2. On considere le voisinage de l'element courant et on choisit le  meilleur d'entre
       eux comme nouvel element courant, parmi ceux absents de la liste tabou, et on l'ajoute
       a la liste tabou
    3. On boucle jusqu'a condition de sortie.
    """
    nb_iter = 0
    
    liste_tabou = list()

    # variables solutions pour la recherche du voisin optimal non tabou
    element_courant = element_initial
    meilleur=element_courant
    meilleur_global=element_courant

    # variables valeurs pour la recherche du voisin optimal non tabou
    valeur_meilleur=0
    valeur_meilleur_global=0

    # variables servant uniquement pour l'affichage
    nb_tabou=0
    meilleur_trouve=0
    meilleur_global_trouve=0
    
    
    while (nb_iter<iter_max):
        nb_iter += 1
        
        valeur_meilleur=0
        
        # on parcours tous les voisins de la solution courante
        for voisin in voisinage(element_courant):
            valeur_voisin=valeur_contenu(voisin)                                                      
                                                                                                      
            # la decomposition en 2 if ne sert qu'a mettre a jour la variable d'affichage nb_tabou    
            # on pourrait combiner les deux avec un and en remplacant le any par all et le == par !=  
            if valeur_voisin>valeur_meilleur:                                                         
                if  any(voisin == tabou for tabou in liste_tabou):                                    
                    nb_tabou+=1                                                                       
                else:                                                                                 
                    # meilleure solution non taboue trouvee                                           
                    meilleur_trouve+=1                                                                
                    valeur_meilleur=valeur_voisin                                                     
                    meilleur=voisin                                                                   
        
        # on met a jour la meilleure solution rencontree depuis le debut
        if valeur_meilleur>valeur_meilleur_global:
            meilleur_global_trouve+=1
            meilleur_global=meilleur
            valeur_meilleur_global=valeur_meilleur

        # on passe au meilleur voisin non tabou trouve
        element_courant=meilleur
        
        # on met a jour la liste tabou
        liste_tabou.append(element_courant) #SOLUTION
        if len(liste_tabou)>=taille_tabou:  #SOLUTION
            liste_tabou.pop(0)              #SOLUTION

    return meilleur_global






    
    