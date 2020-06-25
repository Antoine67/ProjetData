"""Vehicles Routing Problem (VRP) with Time Windows."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from random import randrange
import numpy as np


"""Random adjacency matrix of given size"""
def random_adjacency_matrix(length, minWeight = 1, maxWeight = 2):
    mat = np.random.randint(minWeight,maxWeight+1,(length,length))
    for i,arr in enumerate(mat):
        arr[i] = 0
    return mat

def random_time_window(length, minWeight = 0, maxWeight = 23):
    returnArray = []
    returnArray.append((0,5))
    for i in range(length - 1):
        tuple_a = randrange(minWeight, maxWeight-2)
        tuple_b = randrange(tuple_a+1, maxWeight)
        returnArray.append((tuple_a, tuple_b))
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
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        print(plan_output)
        total_time += solution.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))


class VRPTW:
    
    data = None
    
    def __init__(self, nb_camions,nb_villes, depot=0):
        self.k = nb_camions
        self.towns_nb = nb_villes
        self.depot = depot
       
        
    def create_data_model(self):
       
        data = {}
        data['time_matrix'] = random_adjacency_matrix(self.towns_nb)
        data['time_windows'] = random_time_window(len(data['time_matrix']))
        data['num_vehicles'] = self.k
        data['depot'] = self.depot 
        self.data = data
        
    def pass_matrix(self, matrix, timewindows):
        data = {}
        data['distance_matrix'] = matrix
        data['time_windows'] = timewindows
        data['num_vehicles'] = self.k
        data['depot'] = self.depot 
        self.data = data
        
    def solve(self, strategy, timeout, useTimeout = False):
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(self.data['time_matrix']),
                                               self.data['num_vehicles'], self.data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        # Create and register a transit callback.
        def time_callback(from_index, to_index):
            """Returns the travel time between the two nodes."""
            # Convert from routing variable Index to time matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.data['time_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(time_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Time Windows constraint.
        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            30,  # allow waiting time
            30,  # maximum time per vehicle
            False,  # Don't force start cumul to zero.
            time)
        time_dimension = routing.GetDimensionOrDie(time)
        # Add time window constraints for each location except depot.
        for location_idx, time_window in enumerate(self.data['time_windows']):
            if location_idx == 0:
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        # Add time window constraints for each vehicle start node.
        for vehicle_id in range(self.data['num_vehicles']):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(self.data['time_windows'][0][0],
                                                    self.data['time_windows'][0][1])

        # Instantiate route start and end times to produce feasible times.
        for i in range(self.data['num_vehicles']):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(i)))
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.End(i)))

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        search_parameters.local_search_metaheuristic = strategy
        
        if useTimeout:   
            search_parameters.time_limit.seconds = timeout
            #search_parameters.lns_time_limit.seconds = timeout
        else:
            search_parameters.solution_limit = timeout
            
        search_parameters.log_search = True

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            #print_solution(self.data, manager, routing, solution)
            return solution_to_array(self.data, manager, routing, solution)
        return None
