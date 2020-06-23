from __future__ import print_function
"""Vehicles Routing Problem (VRP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


import matplotlib.pyplot as plt
import numpy as np



"""Random adjacency matrix of given size"""
def random_adjacency_matrix(length, minWeight = 1, maxWeight = 10):
    mat = np.random.randint(minWeight,maxWeight+1,(length,length))
    for i,arr in enumerate(mat):
        arr[i] = 0
    return mat

"""Prints solution on console."""
def print_solution(data, manager, routing, solution):
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))


def solution_to_array(data, manager, routing, solution):
    solut = [None] * data['num_vehicles']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_distance = 0
        
        solut[vehicle_id] = []
        while not routing.IsEnd(index):
            solut[vehicle_id].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        solut[vehicle_id].append(manager.IndexToNode(index))
      
    return solut,route_distance

class VRP:
    
    data = None
    
    def __init__(self, nb_camions,nb_villes, depot=0):
        self.k = nb_camions
        self.towns_nb = nb_villes
        self.depot = depot
       
        
    def create_data_model(self):
       
        data = {}
        data['distance_matrix'] = random_adjacency_matrix(self.towns_nb)
        data['num_vehicles'] = self.k
        data['depot'] = self.depot 
        self.data = data
        
    def pass_matrix(self, matrix):
        data = {}
        data['distance_matrix'] = matrix
        data['num_vehicles'] = self.k
        data['depot'] = self.depot 
        self.data = data
        
    def solve(self, strategy, timeout):
    
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(self.data['distance_matrix']),
                                               self.data['num_vehicles'],
                                               self.data['depot'])
        
        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)
    
    
        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.data['distance_matrix'][from_node][to_node]
    
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
        # Add Distance constraint.
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            1000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)
    
        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (strategy)
        search_parameters.time_limit.seconds = timeout
        #search_parameters.lns_time_limit.seconds = timeout
        search_parameters.log_search = True  
        search_parameters.solution_limit = 100

    
        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
    
        # Print solution on console.
        if solution:
            #print_solution(self.data, manager, routing, solution)
            return solution_to_array(self.data, manager, routing, solution)
        return None
    
   
        
        