import osmnx as ox
from model.RouteModel import Route
from utils import *
from algorithm.RoutingAlgorithm import RoutingAlgorithm
import sys
sys.path.insert(0, '../../server')


class Shortest(RoutingAlgorithm):
    """ Class to perform the shortest route algorithm using ox.shortest_path API

    Args:
        G (GoeData object): a GoeData object that contains data about the search area, 
                            including the start and end points.
    """

    def __init__(self, Geo):
        self.G = Geo.geodata
        self.start = Geo.source
        self.end = Geo.dest

    def search(self,):
        """ The search method is used to find the shortest route between a start and end location.

        Returns:
            Returns:
            shortest_route (Route object) : the obejct that contains the route's path, 
                                    length, and elevation gain
        """
        route = ox.shortest_path(self.G, self.start,
                                 self.end, weight="length")
        shortest_route = Route(get_route_coord(self.G, route), get_path_length(
            self.G, route), get_path_elevation(self.G, route))
        return shortest_route
