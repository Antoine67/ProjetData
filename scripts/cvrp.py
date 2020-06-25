"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from random import randrange
import numpy as np

"""Random adjacency matrix of given size"""
def random_adjacency_matrix(length, minWeight = 1, maxWeight = 10):
    mat = np.random.randint(minWeight,maxWeight+1,(length,length))
    for i,arr in enumerate(mat):
        arr[i] = 0
    return mat

def random_weights(length, minWeight = 1, maxWeight = 10):
        returnArray = []
        returnArray.append(0)
        for i in range(length-1):
            returnArray.append(randrange(minWeight,maxWeight))
        return returnArray

def random_vehiculs(length, arrayIn, minWeight = 0, maxWeight = 0):
        returnArray = []
        if minWeight == 0:
            print("Poids minimum non défini")

        if maxWeight == 0:
            print("Poids maximum non défini")

        if minWeight <= int(sum(arrayIn)/length):
            print("La somme des poids des demandes est supérieurs à la capacité des camions")
            minWeight = int(sum(arrayIn)/length) + 1

        if maxWeight <= minWeight:
            maxWeight = minWeight + 10
            
        tempRandom = randrange(minWeight,maxWeight)
        for i in range(length):
            returnArray.append(tempRandom)
        return returnArray

def solution_to_array(data, manager, routing, solution):
    solut = [None] * data['num_vehicles']
    
    route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)

        solut[vehicle_id] = []
        while not routing.IsEnd(index):
            solut[vehicle_id].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))

            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        solut[vehicle_id].append(manager.IndexToNode(index))
    return solut,route_distance

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))

class CVRP:
    
    data = None
    
    def __init__(self, nb_camions,nb_villes, depot=0):
        self.k = nb_camions
        self.towns_nb = nb_villes
        self.depot = depot
       
        
    def create_data_model(self):
       
        data = {}
        data['distance_matrix'] = random_adjacency_matrix(self.towns_nb)
        data['demands'] = list(random_weights(len(data['distance_matrix'])))
        data['num_vehicles'] = self.k
        data['vehicle_capacities'] = random_vehiculs(data['num_vehicles'], data['demands'])
        data['depot'] = self.depot 
        self.data = data
        
    def pass_matrix(self, matrix, demandMatrix, vehiculsCapacity):
        data = {}
        data['distance_matrix'] = matrix
        data['demands'] = demandMatrix
        data['num_vehicles'] = self.k
        temp = []
        for i in range(data['num_vehicles']):
            temp.append(vehiculsCapacity)
        data['vehicle_capacities'] = temp
        data['depot'] = self.depot 
        self.data = data
        
    def solve(self, strategy, timeout, useTimeout = False):
    
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(self.data['distance_matrix']),
                                               self.data['num_vehicles'],
                                               self.data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return self.data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            self.data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        

        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        
        search_parameters.local_search_metaheuristic = strategy
        
        if useTimeout:   
            search_parameters.time_limit.seconds = timeout
            #search_parameters.lns_time_limit.seconds = timeout
        else:
            search_parameters.solution_limit = timeout
            
        search_parameters.log_search = True
        
        search_parameters.time_limit.seconds = 100
        
        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            #print_solution(self.data, manager, routing, solution)
            return solution_to_array(self.data, manager, routing, solution)
        return None
    
