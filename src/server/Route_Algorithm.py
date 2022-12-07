import numpy as np
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
from keys import google_elevation_api_key
from utils import *


def find_route(source, dest, place, method, percentage, min_max):
    # place = "Piedmont, California, USA"
    G = ox.graph_from_place(place, network_type="all")
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
    route_length = get_path_length(G, route)

    routes = []

    for node in route:
        temp = [G.nodes()[node]['x'], G.nodes()[node]['y']]
        routes.append(temp)
    return routes, route_length


def Astar(source, dest, min_max, percentage, place):
    G = ox.graph_from_place(place, network_type="all")
    G = ox.elevation.add_node_elevations_google(
        G, api_key=google_elevation_api_key)
    G = ox.elevation.add_edge_grades(G)
    start = ox.nearest_nodes(G, source[0], source[1])
    end = ox.nearest_nodes(G, dest[0], dest[1])
    route1 = ox.shortest_path(G, start, end, weight="length")
    route2 = ox.shortest_path(G, start, end, weight="impedance")
    route1_length = get_path_length(G, route1)
    print("asd")
    return route1, route1_length


if __name__ == "__main__":
    place = "Amherst, Massachusetts, USA"
    source = [-72.5198118276834, 42.373051188825855]
    dest = [-72.4992091462399, 42.36979729154845]

    route1, r1_length = find_route(source, dest, place)
    route2, r2_length = Astar(source, dest, 1, 2, place)

    if (route1 == route2):
        print("same")
    else:
        print("different")
    print("done!")
