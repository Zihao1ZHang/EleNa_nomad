from math import *
import osmnx as ox
import networkx as nx


def get_length(G, start, end):
    """ The method calculate the lenght of two adjacent nodes

    Args:
        G (GoeData object): a GoeData object that contains data about the search area, 
                            including the start and end points.
        start (int): node id for the one node
        end (int): node id for the other node

    Returns:
        float: the length of two adjacent nodes
    """
    if nx.is_path(G, [start, end]) == False:
        raise Exception("nodes are not adjacent")

    return G.edges[start, end, 0]['length']


def get_path_length(G, node_list):
    """ The method calculates the total length of a path through a search area

    Args:
        G (GoeData object): a GoeData object that contains data about the search area, 
                            including the start and end points.
        node_list (list of integers):  a list of node IDs that represent the path to be 
                            traversed in sequence

    Returns:
        length (float) : the total length of the path
    """
    if node_list == None or all(isinstance(item, int) for item in node_list) == False or nx.is_path(G, node_list) == False:
        raise Exception("not a valid path")
    length = 0
    for i in range(len(node_list) - 1):
        length += get_length(G, node_list[i], node_list[i + 1])
    return length


def get_path_elevation(G, node_list):
    """ The method calculate the elevation gain of entire path 

    Args:
        G (GoeData object): a GoeData object that contains data about the search area, 
                            including the start and end points.
        start (int): node id for the one node
        end (int): node id for the other node

    Returns:
        total_elevation (float) : the total elevation gain of the path 
    """
    if node_list == None or all(isinstance(item, int) for item in node_list) == False or nx.is_path(G, node_list) == False:
        raise Exception("not a valid path")
    total_elevation = 0
    for i in range(len(node_list) - 1):
        curr_elevation = get_elevation_gain(G, node_list[i], node_list[i + 1])
        if curr_elevation > 0:
            total_elevation += curr_elevation
    return total_elevation


def get_elevation_gain(G, start, end):
    """ The method that calculate the elevation gain of node

    Args:
        G (GoeData object): a GoeData object that contains data about the search area, 
                            including the start and end points.
        start (int): node id for the one node
        end (int): node id for the other node

    Returns:
        elevation (float) : the elevation gain of two nodes
    """
    if nx.is_path(G, [start, end]) == False:
        raise Exception("nodes are not adjacent")
    if start == end:
        return 0
    return G.nodes()[start]['elevation'] - G.nodes()[end]['elevation']


def get_route_coord(G, node_list):
    """ The method that convert node id into coordinates

    Args:
        G (GoeData object): a GoeData object that contains data about the search area, 
                            including the start and end points.
        node_list (list of integers):  a list of node IDs that represent the path to be 
                            traversed in sequence

    Returns:
        route(list) : list contains coordinates, which each coordinate corresponds to a 
                        node in the node_list in the same order
    """
    route = []
    for node in node_list:
        temp = [G.nodes()[node]['x'], G.nodes()[node]['y']]
        route.append(temp)
    return route


def get_result(is_max, routes):
    """ This method compares the routes based on max or min elevation gain

    Args:
        is_max (bool): a boolean value that determines whether the method should return the maximum
                        elevation gain or minimum elevation gain
        routes (list of Route obejct): a list of Route objects that will be compared based on their 
                                        elevation values.

    Returns:
        route (Route obejct): Route object with the maximum or minimum elevation gain value.
    """
    print("get_result")
    if is_max:
        target_elevation = float('-inf')
    else:
        target_elevation = float('inf')
    for route in routes:
        if route:
            if is_max:
                target_elevation = max(target_elevation, route.elevation)
            else:
                target_elevation = min(target_elevation, route.elevation)

    for route in routes:
        if route:
            if target_elevation == route.elevation:
                return route
