from keys import google_elevation_api_key
from utils import *
from model.RouteModel import Route
from model.GeoDataModel import GeoData
from model.NodeWrapperModel import NodeWrapper

import heapq
import osmnx as ox
import networkx as nx
import random
from tqdm import tqdm


def find_route(source, dest, method, percentage=1, is_max=1):
    # Initialize Geo map
    G = GeoData(source, dest, google_elevation_api_key)

    # run routing algorithm
    shortest_route = find_shortest_route(G)
    if method == 'S':
        return shortest_route

    # if method == "A":
    #     routes, _, elevation_g_astar = Astar(G, orig_node, dest_node,
    #                                          is_max, route_length * percentage)
    # elif method == "D":
    #     # routes, _, _ = dijkstra_find_route(G, orig_node, dest_node)\
    #     routes, _, _ = dijkstra_find_route_elevation(
    #         G, orig_node, dest_node, route_length * percentage, is_max=is_max)
    # else:
    #     routes = shortest_routes
    routes_astar, _, elevation_g_astar = Astar(G, orig_node, dest_node, is_max, route_length * percentage)
    routes_dijkstra, elevation_dijkstra, _ = dijkstra_find_route_elevation(
                 G, orig_node, dest_node, route_length * percentage, is_max=is_max)
    routes, elevation_genetic = genetic_algorithm(orig_node, dest_node, G, percentage * route_length)

    print("Elevation gain of Shortest Route: " + str(elevation_g))
    print("Elevation gain of Astar Algortihm: " + str(elevation_g_astar))
    print("Elevation gain of Dijkstra: " + str(elevation_dijkstra))
    print("Elevation gain of Genetic: " + str(elevation_genetic))
    return routes if routes != 0 else shortest_routes


    astar_route = Astar(G, shortest_route.length * percentage, is_max)
    dijkstra_route = dijkstra_find_route_elevation(
        G, shortest_route.length * percentage, is_max)
    
    print("Shortest Route elevatio gain: " + str(shortest_route.elevation))
    if astar_route:
        print("Astar Route elevatio gain: " + str(astar_route.elevation))
    else:
        print("Fail to find route using astar")

    print("Dijkstra Route elevatio gain: " + str(dijkstra_route.elevation))

    # find the route satisified the requirement
    routes = [shortest_route, astar_route, dijkstra_route]
    final_route = get_result(is_max, routes)

    return final_route


def find_shortest_route(Geo):
    route = ox.shortest_path(Geo.geodata, Geo.source,
                             Geo.dest, weight="length")
    shortest_route = Route(get_route_coord(Geo.geodata, route), get_path_length(
        Geo.geodata, route), get_path_elevation(Geo.geodata, route))
    return shortest_route


def Astar(Geo, max_length, is_max=1):
    # create source and destination node
    print("Using Astar Algorithm")
    open_list = [NodeWrapper(Geo.source, is_max)]
    close_list = set()
    visited_node = {Geo.source: NodeWrapper(Geo.source, is_max)}
    while (len(open_list) > 0):
        curr_node = heapq.heappop(open_list)
        close_list.add(curr_node.id)

        if (curr_node.id == Geo.dest):
            path = []
            curr = curr_node
            while curr.parent is not None:
                path.insert(0, curr.id)
                curr = visited_node[curr.parent]
            path.insert(0, curr.id)
            routes = get_route_coord(Geo.geodata, path)
            route_length = get_path_length(Geo.geodata, path)
            elevation_g = get_path_elevation(Geo.geodata, path)
            astar_route = Route(routes, route_length, elevation_g)
            return astar_route

        successors = filter(lambda n: n not in close_list,
                            nx.neighbors(Geo.geodata, curr_node.id))
        for successor in successors:
            distance = curr_node.curr_dist + \
                get_length(Geo.geodata, curr_node.id, successor)
            if distance <= max_length:
                flag = successor in visited_node
                pred_distance = distance + \
                    get_heuristic_distance(Geo.geodata, successor, Geo.dest)
                # elevation_gain = curr_node.elevation + \
                #     get_elevation_gain(Geo.geodata, curr_node.id, successor)
                elevation_gain = curr_node.elevation + \
                    get_elevation_gain(Geo.geodata, curr_node.id, successor)
                successor_node = NodeWrapper(
                    successor, is_max, curr_node.id, distance, pred_distance, elevation_gain, open_list)
                visited_node[successor] = successor_node

                if flag:
                    heapq.heapify(open_list)
                else:
                    heapq.heappush(open_list, successor_node)
    print("Did not find the route")
    return None


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
    shortest_route = Route(get_route_coord(geodata, path), get_path_length(
        geodata, path), get_path_elevation(geodata, path))
    return shortest_route


def dijkstra_find_route_elevation(Geo, max_length, is_max=True, elevation_factor=10, cur_iteration=100):
    if cur_iteration == 0:
        return None
    unvisited_nodes = []
    dist = {}
    _dist = {}
    prev = {}
    distance_traveled = 0
    for node in list(Geo.geodata.nodes.keys()):
        dist[node] = float('inf')
        _dist[node] = float('inf')
        prev[node] = None
        unvisited_nodes.append(node)
    dist[Geo.source] = 0
    _dist[Geo.source] = 0
    while unvisited_nodes is not []:
        current_node = min(dist, key=dist.get)
        distance_traveled += dist[current_node]
        if current_node == Geo.dest:
            break
        unvisited_nodes.remove(current_node)
        for n in nx.neighbors(Geo.geodata, current_node):
            if n in unvisited_nodes:
                if is_max:
                    temp = dist[current_node] + get_length(
                        Geo.geodata, current_node, n) - elevation_factor * get_elevation_gain(G=Geo.geodata, start=Geo.source, end=Geo.dest)
                else:
                    temp = dist[current_node] + get_length(
                        Geo.geodata, current_node, n) + elevation_factor * get_elevation_gain(G=Geo.geodata, start=Geo.source, end=Geo.dest)
                if temp < dist[n]:
                    dist[n] = temp
                    _dist[n] = temp
                    prev[n] = current_node
        dist.pop(current_node)
    path = []
    current_node = Geo.dest
    while current_node:
        path.append(current_node)
        current_node = prev[current_node]
    if get_path_length(geodata, path[::-1]) > max_length:
        return dijkstra_find_route_elevation(geodata, orig, dest, max_length, is_max, elevation_factor/1.5, cur_iteration - 1)
    return get_route_coord(geodata, path[::-1]), get_path_elevation(geodata, path[::-1]), 0


# ********************************************************************* #
# genetic algorithm #
# ********************************************************************* #
# Fitness function that calculates the elevation gain of a route
def calculate_fitness(route, geodata, distance_limit):
    elevation_gain = get_path_elevation(geodata, route)
    distance = get_path_length(geodata, route)
    if distance > distance_limit:
        return elevation_gain / distance
    else:
        return elevation_gain


# Select a route from the population using roulette wheel selection
def select_route(population, geodata, distance_limit):
    # Calculate the total fitness of the population
    total_fitness = sum(calculate_fitness(route, geodata, distance_limit) for route in population)
    # Generate a random number between 0 and the total fitness
    random_num = random.uniform(0, total_fitness)
    # Loop through the population and subtract each route's fitness from the random number
    # until the random number is less than or equal to zero
    for route in population:
        random_num -= calculate_fitness(route, geodata, distance_limit)
        if random_num <= 0:
            return route


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# Combine two routes using crossover
def crossover(route1, route2, geodata):
    same_elements = intersection(route1, route2)
    if len(same_elements) <= 1:
        node1 = random.randint(1, len(route1)-1)
        node2 = random.randint(1, len(route2)-1)
        route_between_nodes = dijkstra_find_route(geodata, route1[node1], route2[node2])
        new_route = route1[:node1 - 1] + route_between_nodes + route2[node2 + 1:]
        return new_route
    rand1, rand2 = random.sample(same_elements, 2)
    left_index1 = route1.index(rand1)
    right_index1 = route1.index(rand2)
    left_index2 = route2.index(rand1)
    right_index2 = route2.index(rand2)
    if left_index1 > right_index1:
        left_index1, right_index1 = right_index1, left_index1
    if left_index2 > right_index2:
        left_index2, right_index2 = right_index2, left_index2
    new_route = route1[:left_index1] + route2[left_index2:right_index2] + route1[right_index1:]
    return new_route


# Mutate a route by randomly changing some of its values
def mutate(route, mutation_probability, geodata):
    # Loop through the route and randomly change the value of each location with a certain probability
    res = []
    for i in range(len(route)):
        if i == 0 or i >= len(route) - 5:
            res.append(route[i])
        elif random.random() < mutation_probability:
            for node in dijkstra_find_route(geodata, route[i-1], route[i+3])[0]:
                if node != route[i-1] and node != route[i+3]:
                    res.append(node)
            i += 3
        else:
            res.append(route[i])
    return res if res != [] else route


# Generate a new population of routes using crossover and mutation
def generate_new_population(old_population, geodata, distance_limit, mutation_probability=0.1):
    new_population = []
    for i in range(len(old_population)):
        # Select two routes to combine using crossover
        route1 = select_route(old_population, geodata, distance_limit)
        route2 = select_route(old_population, geodata, distance_limit)
        new_route = crossover(route1, route2, geodata)
        # Mutate the new route with a small probability
        if random.random() < mutation_probability:
            new_route = mutate(new_route, mutation_probability, geodata)
        if nx.is_path(geodata, new_route):
            new_population.append(new_route)
    return new_population


def generate_population(orig_node, dest_node, geodata, num=100):
    population = []
    rand_node_list = random.sample(list(geodata.nodes.keys()), num)
    for node in rand_node_list:
        route1, _, _ = dijkstra_find_route(geodata, orig_node, node)
        route2, _, _ = dijkstra_find_route(geodata, node, dest_node)
        population.append(route1 + route2[1:])
    return population


# Main loop of the genetic algorithm
def genetic_algorithm(orig_node, dest_node, geodata, distance_limit, max_iteration=10):
    result = []
    res = 0
    population = generate_population(orig_node, dest_node, geodata)
    for i in tqdm(range(max_iteration)):
        population = generate_new_population(population, geodata, distance_limit)
    # Return the route with the highest elevation gain
    for path in population:
        tmp = calculate_fitness(path, geodata, distance_limit)
        if res < tmp:
            res = tmp
            result = path
    return get_route_coord(geodata, result), get_path_elevation(geodata, result)


# if __name__ == "__main__":
    # source = [-72.5198118276834, 42.373051188825855]
    # dest = [-72.4992091462399, 42.36979729154845]
    # G = ox.graph_from_bbox(north=max(source[1], dest[1])+0.01, south=min(
    #     source[1], dest[1])-0.01, east=max(source[0], dest[0])+0.01, west=min(source[0], dest[0])-0.01)
    # G = ox.elevation.add_node_elevations_google(
    #     G, api_key=google_elevation_api_key)
    # G = ox.elevation.add_edge_grades(G)
    #
    # orig_node = ox.nearest_nodes(G, source[0], source[1])
    # dest_node = ox.nearest_nodes(G, dest[0], dest[1])
    #
    # # dest_node = ox.nearest_nodes((dest['x'], dest['y']))
    # route = ox.shortest_path(G, orig_node, dest_node, weight="length")
    # shortest_routes = get_route_coord(G, route)
    # route_length = get_path_length(G, route)
    # elevation_g = get_path_elevation(G, route)
    #
    # res = genetic_algorithm(orig_node, dest_node, G, 1.5*route_length)
    # print(res)
    # route1 = find_route(source, dest, 'A')



    if get_path_length(Geo.geodata, path[::-1]) > max_length:
        return dijkstra_find_route_elevation(Geo, max_length, is_max, elevation_factor/1.5, cur_iteration - 1)
    path = path[::-1]
    routes = get_route_coord(Geo.geodata, path)
    route_length = get_path_length(Geo.geodata, path)
    elevation_g = get_path_elevation(Geo.geodata, path)
    dijkstra_route = Route(routes, route_length, elevation_g)
    return dijkstra_route


if __name__ == "__main__":
    place = "Amherst, Massachusetts, USA"
    # source = [-72.5198118276834, 42.373051188825855]
    # dest = [-72.4992091462399, 42.36979729154845]
    source = [-72.50962524612441, 42.375880221431004]
    dest = [-72.49934702117964, 42.370442879663926]

    route1 = find_route(source, dest, method='A', percentage=1.5, is_max=0)
