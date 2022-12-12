from math import *
import osmnx as ox


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

    circle_dist = ox.distance.great_circle_vec(
        n1['y'], n1['x'], n2['y'], n2['x'])
    return circle_dist


def get_result(is_max, routes):
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


class NodeWrapper(object):
    def __init__(self, node, is_max, parent=None, curr_dist=0, pred_distance=0, elevation=0, route_path=None):
        self.id = node
        self.parent = parent
        self.curr_dist = curr_dist
        self.elevation = elevation
        self.route_path = route_path
        self.pred_dist = pred_distance
        self.is_max = is_max

    def __lt__(self, other):
        """Operation override for the less than operation to compare two objects of the same type.

        Args:
            other: another object of the NodeIdWrapper time, with which current object has to be compared

        Returns:
            A boolean representing if the current node is less than the other node
        """

        if self.is_max:
            # print("find max elevation")
            self_heuristic_dist = self.pred_dist + self.elevation * 10
            other_heuristic_dist = other.pred_dist + other.elevation * 10
            return self_heuristic_dist > other_heuristic_dist
        else:
            self_heuristic_dist = self.elevation + self.pred_dist
            other_heuristic_dist = other.elevation + other.pred_dist
            return self_heuristic_dist < other_heuristic_dist
