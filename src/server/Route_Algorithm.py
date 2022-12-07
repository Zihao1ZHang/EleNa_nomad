import numpy as np
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point


def find_route(source, dest, place):
    # place = "Piedmont, California, USA"
    G = ox.graph_from_place(place, network_type="all")
    print(source)
    print(dest)
    orig_node = ox.nearest_nodes(G, source[0], source[1])
    dest_node = ox.nearest_nodes(G, dest[0], dest[1])
    print(orig_node)
    print(dest_node)

    # dest_node = ox.nearest_nodes((dest['x'], dest['y']))
    route = ox.shortest_path(G, orig_node, dest_node, weight="length", cpus=8)
    routes = []

    for node in route:
        temp = [G.nodes()[node]['x'], G.nodes()[node]['y']]
        routes.append(temp)
    return routes


# if __name__ == "__main__":
#     place = "Amherst, Massachusetts, USA"
#     source = {'x': -72.5198118276834, 'y':  42.373051188825855}
#     dest = {'x': -72.4992091462399, 'y': 42.36979729154845}

#     routes = find_route(source, dest, place)
#     print("done!")
if __name__ == "__main__":
    s = [-72.50111727912923, 42.37282871002975]
    d = [-72.48302846153265, 42.3650288487147]
    p = "Amherst, Massachusetts, USA"
    g = ox.graph_from_place(p, network_type="all")
    node_1 = ox.nearest_nodes(g, s[0], s[1])
    node_2 = ox.nearest_nodes(g, d[0], d[1])
    route = ox.shortest_path(g, node_1, node_2, weight="length", cpus=8)
