from algorithm.RoutingAlgorithm import RoutingAlgorithm
from utils import *
from model.RouteModel import Route
from model.NodeWrapperModel import NodeWrapper
import networkx as nx
import heapq
import sys
sys.path.insert(0, '../../server')


class Astar(RoutingAlgorithm):
    def __init__(self, Geodata, distance_limit, is_max):
        self.G = Geodata.geodata
        self.start = Geodata.source
        self.end = Geodata.dest
        self.distance_limit = distance_limit
        self.is_max = is_max

    def search(self,):
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
                        get_heuristic_distance(
                            self.G, successor, self.end)
                    # elevation_gain = curr_node.elevation + \
                    #     get_elevation_gain(Geo.geodata, curr_node.id, successor)
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
