import heapq
import networkx as nx
from src.server.model.NodeWrapperModel import NodeWrapper
from src.server.model.RouteModel import Route
from src.server.utils import *
from src.server.algorithm.RoutingAlgorithm import RoutingAlgorithm
import sys
sys.path.insert(0, '../../server')


class Astar(RoutingAlgorithm):
    """Class to perform the complete weighted A* search

    Attributes:
        Geodata: The instance of Geodatamodel, contains data for the search area,
                starting point, and destination point
        distance_limit: The max distance that the aglorithm can go
        is_max: Find the max elevation or minimum elevation
    """

    def __init__(self, Geodata, distance_limit, is_max):
        self.G = Geodata.geodata
        self.start = Geodata.source
        self.end = Geodata.dest
        self.distance_limit = distance_limit
        self.is_max = is_max

    def get_heuristic_distance(self, G, node1, node2):
        """ This function calculates the heuristic distance between two nodes in a graph G.
            The distance is calculated using the great circle distance formula. The nodes are
            specified by their indices node1 and node2 in the list of nodes of the graph G.
            The function returns the heuristic distance between the two nodes.

        Args:
            G (GoeData object): model that contains data of searching area, start, and end point
            start (int): node id for the one node
            end (int): node id for the other node

        Returns:
            circle_dist(float) : the heuristic distance between the two nodes
        """
        n1 = G.nodes()[node1]
        n2 = G.nodes()[node2]

        circle_dist = ox.distance.great_circle_vec(
            n1['y'], n1['x'], n2['y'], n2['x'])
        return circle_dist

    def search(self,):
        """The function to execute weeighted A* algorithm

        Returns:
            astar_route(Route object) : the obejct that contains the route's path,
                                    length, and elevation gain
            None : if did not find the route
        """
        print("Using Astar Algorithm")
        open_list = [NodeWrapper(self.start, self.is_max)]
        close_list = set()
        visited_node = {self.start: NodeWrapper(
            self.start, self.is_max)}
        while (len(open_list) > 0):
            curr_node = heapq.heappop(open_list)
            close_list.add(curr_node.id)

            if (curr_node.id == self.end):
                path = []
                curr = curr_node
                while curr.parent is not None:
                    path.insert(0, curr.id)
                    curr = visited_node[curr.parent]
                path.insert(0, curr.id)
                routes = get_route_coord(self.G, path)
                route_length = get_path_length(self.G, path)
                elevation_g = get_path_elevation(self.G, path)
                astar_route = Route(routes, route_length, elevation_g)
                return astar_route

            successors = filter(lambda n: n not in close_list,
                                nx.neighbors(self.G, curr_node.id))
            for successor in successors:
                distance = curr_node.curr_dist + \
                    get_length(self.G, curr_node.id, successor)
                if distance <= self.distance_limit:
                    flag = successor in visited_node
                    pred_distance = distance + \
                        self.get_heuristic_distance(
                            self.G, successor, self.end)
                    elevation_gain = curr_node.elevation + \
                        get_elevation_gain(
                            self.G, curr_node.id, successor)
                    successor_node = NodeWrapper(
                        successor, self.is_max, curr_node.id, distance, pred_distance, elevation_gain, open_list)
                    visited_node[successor] = successor_node

                    if flag:
                        heapq.heapify(open_list)
                    else:
                        heapq.heappush(open_list, successor_node)
        return None
