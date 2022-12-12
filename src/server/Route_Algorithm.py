import numpy as np
import heapq
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
from keys import google_elevation_api_key
from utils import *
import networkx as nx
from model.Route import Route


def find_route(source, dest, method='D', percentage=1, is_max=1):
    G = ox.graph_from_bbox(north=max(source[1], dest[1])+0.01, south=min(
        source[1], dest[1])-0.01, east=max(source[0], dest[0])+0.01, west=min(source[0], dest[0])-0.01)
    G = ox.elevation.add_node_elevations_google(
        G, api_key=google_elevation_api_key)
    G = ox.elevation.add_edge_grades(G)
    print(source)
    print(dest)
    orig_node = ox.nearest_nodes(G, source[0], source[1])
    dest_node = ox.nearest_nodes(G, dest[0], dest[1])
    print(orig_node)
    print(dest_node)

    # dest_node = ox.nearest_nodes((dest['x'], dest['y']))
    route = ox.shortest_path(G, orig_node, dest_node, weight="length")
    shortest_route = Route(get_route_coord(G, route), get_path_length(
        G, route), get_path_elevation(G, route))
    route_astar = Astar(G, orig_node, dest_node,
                        is_max, shortest_route.length * percentage)
    route_dijkstra = dijkstra_find_route_elevation(
        G, orig_node, dest_node, shortest_route.length * percentage, is_max=is_max)

    print("*************************")
    print(shortest_route.elevation)
    print(route_dijkstra.elevation)
    print("*************************")

    routes = [shortest_route]
    if (route_astar):
        routes.append(route_astar)
    if (route_dijkstra):
        routes.append(route_dijkstra)

    routes = get_result(is_max, routes)

    return routes


def Astar(G, start, end, is_max, max_length):
    # create source and destination node
    print("Using Astar Algorithm")
    open_list = [NodeWrapper(start, is_max)]
    close_list = set()
    visited_node = {start: NodeWrapper(start, is_max)}
    while (len(open_list) > 0):
        curr_node = heapq.heappop(open_list)
        close_list.add(curr_node.id)

        if (curr_node.id == end):
            path = []
            curr = curr_node
            while curr.parent is not None:
                path.insert(0, curr.id)
                curr = visited_node[curr.parent]
            path.insert(0, curr.id)
            routes = get_route_coord(G, path)
            route_length = get_path_length(G, path)
            elevation_g = get_path_elevation(G, path)
            astar_route = Route(routes, route_length, elevation_g)
            return astar_route

        successors = filter(lambda n: n not in close_list,
                            nx.neighbors(G, curr_node.id))
        for successor in successors:
            distance = curr_node.curr_dist + \
                get_length(G, curr_node.id, successor)
            if distance <= max_length:
                flag = successor in visited_node
                pred_distance = distance + \
                    get_heuristic_distance(G, successor, end)
                elevation_gain = curr_node.elevation + \
                    get_elevation_gain(G, curr_node.id, successor)
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


def dijkstra_find_route_elevation(geodata, orig, dest, max_length, is_max=True, elevation_factor=10, cur_iteration=100):
    if cur_iteration == 0:
        return None
    unvisited_nodes = []
    dist = {}
    _dist = {}
    prev = {}
    distance_traveled = 0
    for node in list(geodata.nodes.keys()):
        dist[node] = float('inf')
        _dist[node] = float('inf')
        prev[node] = None
        unvisited_nodes.append(node)
    dist[orig] = 0
    _dist[orig] = 0
    while unvisited_nodes is not []:
        current_node = min(dist, key=dist.get)
        distance_traveled += dist[current_node]
        if current_node == dest:
            break
        unvisited_nodes.remove(current_node)
        for n in nx.neighbors(geodata, current_node):
            if n in unvisited_nodes:
                if is_max:
                    temp = dist[current_node] + get_length(
                        geodata, current_node, n) - elevation_factor * get_elevation_gain(G=geodata, start=orig, end=dest)
                else:
                    temp = dist[current_node] + get_length(
                        geodata, current_node, n) + elevation_factor * get_elevation_gain(G=geodata, start=orig, end=dest)
                if temp < dist[n]:
                    dist[n] = temp
                    _dist[n] = temp
                    prev[n] = current_node
        dist.pop(current_node)
    path = []
    current_node = dest
    while current_node:
        path.append(current_node)
        current_node = prev[current_node]
    if get_path_length(geodata, path[::-1]) > max_length:
        return dijkstra_find_route_elevation(geodata, orig, dest, max_length, is_max, elevation_factor/1.5, cur_iteration - 1)
    path = path[::-1]
    routes = get_route_coord(geodata, path)
    route_length = get_path_length(geodata, path)
    elevation_g = get_path_elevation(geodata, path)
    print("Dijkstra")
    print(route_length)
    print(elevation_g)
    # print(path)
    dijkstra_route = Route(routes, route_length, elevation_g)
    return dijkstra_route


if __name__ == "__main__":
    place = "Amherst, Massachusetts, USA"
    # source = [-72.5198118276834, 42.373051188825855]
    # dest = [-72.4992091462399, 42.36979729154845]
    source = [-72.50962524612441, 42.375880221431004]
    dest = [-72.49934702117964, 42.370442879663926]

    route1 = find_route(source, dest, 'A')
