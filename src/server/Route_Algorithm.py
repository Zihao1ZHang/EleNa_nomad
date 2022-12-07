import numpy as np
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point


def find_route(source, dest, place):
    # place = "Piedmont, California, USA"
    # G = ox.graph_from_place(place, network_type="all")
    print(source)
    print(dest)
    # G = ox.graph_from_place(place, network_type="all")
    G = ox.graph_from_bbox(north=max(source[1], dest[1])+0.01, south=min(source[1], dest[1])-0.01, east=max(source[0], dest[0])+0.01, west=min(source[0], dest[0])-0.01)
    orig_node = ox.nearest_nodes(G, source[0], source[1])
    dest_node = ox.nearest_nodes(G, dest[0], dest[1])
    print(orig_node)
    print(dest_node)

    # dest_node = ox.nearest_nodes((dest['x'], dest['y']))
    route = dijkstra_find_route(G, orig_node, dest_node)
    # route = ox.shortest_path(G, orig_node, dest_node, weight="length", cpus=8)
    routes = []

    for node in route:
        temp = [G.nodes()[node]['x'], G.nodes()[node]['y']]
        routes.append(temp)
    return routes


def get_length(G, start, end):
    return G.edges[start, end, 0]['length']


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
                temp = dist[current_node] + get_length(geodata, current_node, n)
                if temp < dist[n]:
                    dist[n] = temp
                    prev[n] = current_node
        dist.pop(current_node)
    path = []
    current_node = dest
    while current_node:
        path.append(current_node)
        current_node = prev[current_node]
    return path[::-1]




# if __name__ == "__main__":
#     place = "Amherst, Massachusetts, USA"
#     source = {'x': -72.5198118276834, 'y':  42.373051188825855}
#     dest = {'x': -72.4992091462399, 'y': 42.36979729154845}

#     routes = find_route(source, dest, place)
#     print("done!")
# if __name__ == "__main__":
    # s = [-72.50111727912923, 42.37282871002975]
    # d = [-72.48302846153265, 42.3650288487147]
    # p = "Amherst, Massachusetts, USA"
    # ox.config(use_cache=True, log_console=True)
    # g = ox.graph_from_place(p, network_type="all")
    # node_1 = ox.nearest_nodes(g, s[0], s[1])
    # node_2 = ox.nearest_nodes(g, d[0], d[1])
    # route = ox.shortest_path(g, node_1, node_2, weight="length", cpus=8)
