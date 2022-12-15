import pytest
import unittest
import osmnx as ox
import sys

sys.path.insert(1, './src')
from server.model.GeoDataModel import GeoData
from server.model.RouteModel import Route
from server.model.keys import google_elevation_api_key
import server.Route_Algorithm as RA

from server.algorithm.genetic_algorithm import GeneticAlgorithm
from server.algorithm.Astar_algorithm import Astar
from server.algorithm.Dijkstra_algorithm import Dijkstra
from server.algorithm.Shortest_algorithm import Shortest

class TestRouteAlgorithm(unittest.TestCase):

    geoDataModel = None
    routeModel = None
    
    # Different Routes
    aStar = None
    shortest = None
    dijkstra = None
    genetic = None

    # Percentage of shortest
    distance_limit = 0

    def InitializeModel(self, source, dest, percentage=1):
        self.geoDataModel = GeoData(source, dest, google_elevation_api_key)
        self.shortest = Shortest(self.geoDataModel)
        self.distance_limit = self.shortest.search().length


        self.aStar = Astar(self.geoDataModel, self.distance_limit * percentage, 1)
        self.dijkstra = Dijkstra(self.geoDataModel, self.distance_limit * percentage, 1)
        self.genetic = GeneticAlgorithm(self.geoDataModel, self.distance_limit * percentage, 1)

    def test_InputValidation():
        pass

    # Each routing algorithm should end up at the same point
    def test_RouteSameSourceDestination(self):
        # Initialize routes with source, destination, and maximum distance
        self.InitializeModel((42.687672, -71.121567), (42.687672, -71.121567))
        
        # All routes found
        routeShortest = self.shortest.search()
        routeAStar = self.aStar.search()
        routeDijkstra = self.dijkstra.search(elevation_factor=10, cur_iteration=100)
        routeGenetic = self.genetic.cal_result()
        all_routes = [routeShortest, routeAStar, routeDijkstra, routeGenetic]

        # Verify that each route is valid
        for route in all_routes:
            if route != None:
                assert route.length <= self.distance_limit
                assert route[-1] == self.geoDataModel.dest
        
        # Compare elevation of route determined by elevation
        # Compare node for node
        
    
    def test_StraightRoute(self):
        pass
        
