from math import *


def get_length(G, start, end):
    return G.edges[start, end, 0]['length']


def get_path_length(G, node_list):
    length = 0
    for i in range(len(node_list) - 1):
        length += get_length(G, node_list[i], node_list[i + 1])
    return length


def get_path_elevation(G, node_list):
    total_elevation = 0
    for i in range(len(node_list) - 1):
        curr_elevation = get_elevation_gain(G, node_list[i], node_list[i + 1])
        if curr_elevation > 0:
            total_elevation += curr_elevation
    return total_elevation


def get_route_coord(G, node_list):
    routes = []
    for node in node_list:
        temp = [G.nodes()[node]['x'], G.nodes()[node]['y']]
        routes.append(temp)
    return routes


def get_elevation_gain(G, start, end):
    if start == end:
        return 0
    return G.nodes()[start]['elevation'] - G.nodes()[end]['elevation']


def get_heuristic_distance(G, node1, node2):
    n1 = G.nodes()[node1]
    n2 = G.nodes()[node2]
    R = 6737000
    dlon = n1['y'] - n2['y']
    dlat = n1['x'] - n2['x']
    a = (sin(dlat/2))**2 + cos(n1['x']) * cos(n2['x']) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
    # return sqrt((n1['x'] - n2['x']) ** 2 + (n1['y'] - n2['y']) ** 2)


class NodeWrapper(object):
    def __init__(self, node, parent=None, curr_dist=0, pred_distance=0, elevation=0, route_path=None):
        self.id = node
        self.parent = parent
        self.curr_dist = curr_dist
        self.elevation = elevation
        self.route_path = route_path
        self.pred_dist = pred_distance

    def __lt__(self, other):
        """Operation override for the less than operation to compare two objects of the same type.

        Args:
            other: another object of the NodeIdWrapper time, with which current object has to be compared

        Returns:
            A boolean representing if the current node is less than the other node
        """
        self_heuristic_dist = self.elevation
        other_heuristic_dist = other.elevation
        return self_heuristic_dist > other_heuristic_dist
