import math
import sys
sys.path.insert(0, '../../server')
from src.server.utils import *
from src.server.model.RouteModel import Route
import networkx as nx
import random
from tqdm import tqdm


class GeneticAlgorithm(object):
    """Class to perform the genetic algorithm

    Attributes:
    Geo: The instance of Geodatamodel, contains data for the search area,
    distance_limit: The max distance that the aglorithm can go
    is_max: Find the max elevation or minimum elevation
    max_iteration: The number of populations generated
    """

    def __init__(self, geo, distance_limit, is_max, max_iteration=10):
        self.geodata = geo.geodata
        self.orig_node = geo.source
        self.dest_node = geo.dest
        self.distance_limit = distance_limit
        self.max_iteration = max_iteration
        self.is_max = is_max

    def set_orig(self, orig_node):
        self.orig_node = orig_node

    def set_dest(self, dest_node):
        self.dest_node = dest_node

    def set_distance_limit(self, distance_limit):
        self.distance_limit = distance_limit

    def set_geodata(self, geodata):
        self.geodata = geodata

    def set_maxit(self, maxit):
        self.max_iteration = maxit

    def calculate_fitness(self, route):
        """The function to calculate the fitness of a given route in a graph.

        Args:
            route: A list of nodes representing the path to evaluate

        Returns:
            elevation_gain: The fitness of the given route
        """
        if self.is_max is True:
            elevation_gain = get_path_elevation(self.geodata, route)
        else:
            elevation_gain = get_path_elevation(self.geodata, route)
            if elevation_gain != 0:
                elevation_gain = math.exp(-10*get_path_elevation(self.geodata, route))
        distance = get_path_length(self.geodata, route)
        if distance > self.distance_limit:
            return elevation_gain / distance
        else:
            return elevation_gain

    def select_route(self, population):
        """The function to select a route from the population using roulette wheel selection.

        Args:
            population: A list of routes to select from

        Returns:
            route: The selected route
        """
        # Calculate the total fitness of the population
        total_fitness = sum(self.calculate_fitness(route) for route in population)
        # Generate a random number between 0 and the total fitness
        random_num = random.uniform(0, total_fitness)
        # Loop through the population and subtract each route's fitness from the random number
        # until the random number is less than or equal to zero
        for route in population:
            random_num -= self.calculate_fitness(route)
            if random_num <= 0:
                return route

    def crossover(self, route1, route2):
        """The function to combine two routes using crossover.

        Args:
            route1: The first route selected to perform crossover operation
            route2: The second route selected to perform crossover operation

        Returns:
            new_route: The generated route after crossover
        """
        # Find intersection of route1 and route2
        same_elements = self.intersection(route1, route2)
        if len(same_elements) <= 1:
            # If no intersection is found, randomly select two nodes from the routes and find the shortest route
            # between them. The resulting route is then inserted between the two selected nodes in the original
            # routes, and the new route is returned.
            node1 = random.randint(1, len(route1)-1)
            node2 = random.randint(1, len(route2)-1)
            route_between_nodes = self.dijkstra_find_route(self.geodata, route1[node1], route2[node2])
            new_route = route1[:node1 - 1] + route_between_nodes + route2[node2 + 1:]
            return new_route
        # If intersection is found, randomly sample two nodes from the intersection, and finds their indices in the
        # two routes. The new route is then constructed by combining route1 and route2 together using these indexes
        rand1, rand2 = random.sample(same_elements, 2)
        left_index1 = route1.index(rand1)
        right_index1 = route1.index(rand2)
        left_index2 = route2.index(rand1)
        right_index2 = route2.index(rand2)
        # If the indices are in reverse order, the function swaps them to ensure that the left index is smaller than
        # the right index.
        if left_index1 > right_index1:
            left_index1, right_index1 = right_index1, left_index1
        if left_index2 > right_index2:
            left_index2, right_index2 = right_index2, left_index2
        new_route = route1[:left_index1] + route2[left_index2:right_index2] + route1[right_index1:]
        return new_route

    def mutate(self, route, mutation_probability):
        """The function to mutate a route.

        Args:
            route: The route selected to perform mutation operation
            mutation_probability: The probability a node is mutated

        Returns:
            new_route: The generated route after mutation
        """
        res = []
        for i in range(len(route)):
            # Loop through the route and randomly delete some nodes and then connect the route using shortest route
            if i == 0 or i >= len(route) - 5:
                res.append(route[i])
            elif random.random() < mutation_probability:
                for node in self.dijkstra_find_route(self.geodata, route[i-1], route[i+3])[0]:
                    if node != route[i-1] and node != route[i+3]:
                        res.append(node)
                i += 3
            else:
                res.append(route[i])
        return res if res != [] else route

    def generate_new_population(self, old_population, mutation_probability=0.1):
        """The function to generate a new population of routes using crossover and mutation.

        Args:
            old_population: A list of routes selected to generate new population
            mutation_probability: The probability a route is mutated

        Returns:
            new_population: The generated list of routes
        """
        new_population = []
        for i in range(len(old_population)):
            # Select two routes to combine using crossover
            route1 = self.select_route(old_population)
            route2 = self.select_route(old_population)
            new_route = self.crossover(route1, route2)
            # Mutate the new route with a small probability
            if random.random() < mutation_probability:
                new_route = self.mutate(new_route, mutation_probability)
            if nx.is_path(self.geodata, new_route):
                new_population.append(new_route)
        return new_population

    def generate_population(self, num=100):
        """The function to initailize the first population.

        Args:
            num: number of routes to generate

        Returns:
            population: The generated list of routes
        """
        population = []
        # Randomly select a node in the graph and connect startpoint, this node and destination using shortest route
        rand_node_list = random.choices(list(self.geodata.nodes.keys()), k=num)
        for node in rand_node_list:
            route1, _, _ = self.dijkstra_find_route(self.geodata, self.orig_node, node)
            route2, _, _ = self.dijkstra_find_route(self.geodata, node, self.dest_node)
            population.append(route1 + route2[1:])
        return population

    def cal_result(self):
        """The function to perform the genetic algorithm.

        Returns:
            generic_route: The route calculated by genetic algorithm
        """
        result = []
        res = 0
        population = self.generate_population()
        for i in tqdm(range(self.max_iteration)):
            population = self.generate_new_population(population)
        # Return the route with the highest/lowest elevation gain
        for path in population:
            tmp = self.calculate_fitness(path)
            if res < tmp:
                res = tmp
                result = path
        routes = get_route_coord(self.geodata, result)
        route_length = get_path_length(self.geodata, result)
        if route_length > self.distance_limit:
            return None
        elevation_g = get_path_elevation(self.geodata, result)
        genetic_route = Route(routes, route_length, elevation_g)
        return genetic_route

    # A funtion to find intersection of two lists
    @staticmethod
    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    # Dijkstra algorithm to find shortest route
    @staticmethod
    def dijkstra_find_route(geodata, orig, dest):
        unvisited_nodes = []
        dist = {}
        prev = {}
        for node in list(geodata.nodes.keys()):
            dist[node] = float('inf')
            prev[node] = None
            unvisited_nodes.append(node)
        dist[orig] = 0
        while unvisited_nodes is not []:
            current_node = min(dist, key=dist.get)
            if current_node == dest:
                break
            unvisited_nodes.remove(current_node)
            for n in nx.neighbors(geodata, current_node):
                if n in unvisited_nodes:
                    temp = dist[current_node] + \
                           get_length(geodata, current_node, n)
                    if temp < dist[n]:
                        dist[n] = temp
                        prev[n] = current_node
            dist.pop(current_node)
        path = []
        current_node = dest
        while current_node:
            path.append(current_node)
            current_node = prev[current_node]
        path = path[::-1]
        return path, 0, 0
