import sys
sys.path.insert(0, '../../server')
from algorithm.RoutingAlgorithm import RoutingAlgorithm
from utils import *
from model.RouteModel import Route
import osmnx as ox
import sys
sys.path.insert(0, '../../server')


class Shortest(RoutingAlgorithm):
    def __init__(self, Geo):
        self.G = Geo.geodata
        self.start = Geo.source
        self.end = Geo.dest

    def search(self,):
        route = ox.shortest_path(self.G, self.start,
                                 self.end, weight="length")
        shortest_route = Route(get_route_coord(self.G, route), get_path_length(
            self.G, route), get_path_elevation(self.G, route))
        return shortest_route
