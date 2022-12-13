from algorithm.RoutingAlgorithm import RoutingAlgorithm
from utils import *
from model.RouteModel import Route
import networkx as nx
import sys
sys.path.insert(0, '../../server')


class Dijkstra(RoutingAlgorithm):
    def __init__(self, Geo, distance_limit, is_max=True):
        self.G = Geo.geodata
        self.start = Geo.source
        self.end = Geo.dest
        self.distance_limit = distance_limit
        self.is_max = is_max

    def search(self, elevation_factor, cur_iteration):
        if cur_iteration == 0:
            return None
        unvisited_nodes = []
        dist = {}
        _dist = {}
        prev = {}
        distance_traveled = 0
        for node in list(self.G.nodes.keys()):
            dist[node] = float('inf')
            _dist[node] = float('inf')
            prev[node] = None
            unvisited_nodes.append(node)
        dist[self.start] = 0
        _dist[self.start] = 0
        while unvisited_nodes is not []:
            current_node = min(dist, key=dist.get)
            distance_traveled += dist[current_node]
            if current_node == self.end:
                break
            unvisited_nodes.remove(current_node)
            for n in nx.neighbors(self.G, current_node):
                if n in unvisited_nodes:
                    if self.is_max:
                        temp = dist[current_node] + get_length(
                            self.G, current_node, n) - elevation_factor * get_elevation_gain(G=self.G, start=self.start, end=self.end)
                    else:
                        temp = dist[current_node] + get_length(
                            self.G, current_node, n) + elevation_factor * get_elevation_gain(G=self.G, start=self.start, end=self.end)
                    if temp < dist[n]:
                        dist[n] = temp
                        _dist[n] = temp
                        prev[n] = current_node
            dist.pop(current_node)
        path = []
        current_node = self.end
        while current_node:
            path.append(current_node)
            current_node = prev[current_node]
        if get_path_length(self.G, path[::-1]) > self.distance_limit:
            return self.search(elevation_factor/1.5, cur_iteration - 1)
        path = path[::-1]
        routes = get_route_coord(self.G, path)
        route_length = get_path_length(self.G, path)
        elevation_g = get_path_elevation(self.G, path)
        dijkstra_route = Route(routes, route_length, elevation_g)
        return dijkstra_route
