import numpy as np
import osmnx as ox


def find_route(source, dest, place):
    # place = "Piedmont, California, USA"
    G = ox.graph_from_place(place, network_type="drive")

    print(source)
    print(dest)
    orig_node = ox.distance.nearest_nodes(G, source['x'], source['y'])
    dest_node = ox.distance.nearest_nodes(G, dest['x'], dest['y'])

    # dest_node = ox.nearest_nodes((dest['x'], dest['y']))
    route = ox.shortest_path(G, orig_node, dest_node, weight="length")
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
