from keys import google_elevation_api_key
from utils import *
from model.RouteModel import Route
from model.GeoDataModel import GeoData
from model.NodeWrapperModel import NodeWrapper
from algorithm.genetic_algorithm import GeneticAlgorithm

import heapq
import osmnx as ox
import networkx as nx


def find_route(source, dest, method, percentage=1, is_max=1):
    # Initialize Geo map
    G = GeoData(source, dest, google_elevation_api_key)
    # run routing algorithm
    shortest_route = find_shortest_route(G)
    if method == 'S':
        return shortest_route
    astar_route = Astar(G, shortest_route.length * percentage, is_max)
    dijkstra_route = dijkstra_find_route_elevation(
        G, shortest_route.length * percentage, is_max)
    genetic = GeneticAlgorithm(G, shortest_route.length * percentage, is_max)
    genetic_route = genetic.cal_result()

    print("Shortest Route elevatio gain: " + str(shortest_route.elevation))
    print("Maxium length allowed: " + str(shortest_route.length * percentage))
    if astar_route:
        print("Astar Route elevatio gain: " + str(astar_route.elevation))
        print("Astar Route length: " + str(astar_route.length))
    else:
        print("Fail to find route using astar")

    print("Dijkstra Route length: " + str(dijkstra_route.length))
    print("Genetic Route length: " + str(genetic_route.length))
    print("Dijkstra Route elevatio gain: " + str(dijkstra_route.elevation))
    print("Genetic Route elevatio gain: " + str(genetic_route.elevation))


    # find the route satisified the requirement
    routes = [shortest_route, astar_route, dijkstra_route, genetic_route]
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
    if get_path_length(Geo.geodata, path[::-1]) > max_length:
        return dijkstra_find_route_elevation(Geo, max_length, is_max, elevation_factor/1.5, cur_iteration - 1)
    path = path[::-1]
    routes = get_route_coord(Geo.geodata, path)
    route_length = get_path_length(Geo.geodata, path)
    elevation_g = get_path_elevation(Geo.geodata, path)
    dijkstra_route = Route(routes, route_length, elevation_g)
    return dijkstra_route


if __name__ == "__main__":
    # source = [-72.5198118276834, 42.373051188825855]
    # dest = [-72.4992091462399, 42.36979729154845]
    source = [-72.50962524612441, 42.375880221431004]
    dest = [-72.49934702117964, 42.370442879663926]

    route1 = find_route(source, dest, method='A', percentage=1.5, is_max=0)
