import pytest
import unittest
import osmnx as ox
import sys
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append('C:/Users/erich/Documents/2022_FALL/CS520_Software_Engineering/final/EleNa_nomad/src/server')
from utils import *
from model.GeoDataModel import GeoData
from model.RouteModel import Route
from model.keys import google_elevation_api_key
import Route_Algorithm as RA

from algorithm.genetic_algorithm import GeneticAlgorithm
from algorithm.Astar_algorithm import Astar
from algorithm.Dijkstra_algorithm import Dijkstra
from algorithm.Shortest_algorithm import Shortest

class TestRouteAlgorithms(unittest.TestCase):

    geoDataModel = None
    routeModel = None
    
    # Different Routes
    aStar = None
    shortest = None
    dijkstra = None
    genetic = None

    # Percentage of shortest
    distance_limit = 0

    # Simple G
    G = nx.MultiDiGraph()
    G.add_node(1, x='A', y='TEST', elevation=0)
    G.add_node(2, x='B', y='TEST', elevation=10)
    G.add_node(3, x='C', y='TEST', elevation=20)
    G.add_edge(1, 3, length=5.0)
    G.add_edge(1, 2, length=2.0)
    G.add_edge(2, 3, length=2.0)

    # Disconnected G
    G_disconnected = nx.MultiDiGraph()
    G_disconnected.add_node(1, x='A', y='TEST', elevation=0)
    G_disconnected.add_node(2, x='B', y='TEST', elevation=10)
    G_disconnected.add_node(3, x='C', y='TEST', elevation=20)
    G_disconnected.add_edge(1, 2, length=2.0)

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
    # edge_labels=dict([((u,v,),d['length'])
    #          for u,v,d in G.edges(data=True)])
    # plt.show()

    # Define the source, destination
    def InitializeModel(self, source, dest, G, percentage=1):
        self.geoDataModel = GeoData(source, dest, google_elevation_api_key, G, True)
        self.shortest = Shortest(self.geoDataModel)
        self.distance_limit = self.shortest.search().length

        self.aStar = Astar(self.geoDataModel, self.distance_limit * percentage, 1)
        self.dijkstra = Dijkstra(self.geoDataModel, self.distance_limit * percentage, 1)
        self.genetic = GeneticAlgorithm(self.geoDataModel, self.distance_limit * percentage, 1)

    """ Same Start and End Node """
    def test_Dijkstra_AA(self):
        # Initialize routes with same source and destination
        #self.distance_limit = 0.0
        self.InitializeModel(1, 1, self.G)
        
        # All routes found
        routeDijkstra = self.dijkstra.search(elevation_factor=10, cur_iteration=100)

        G = self.geoDataModel

        # Verify that each route is valid
        node = self.geoDataModel.dest
        assert routeDijkstra != None
        assert routeDijkstra.length <= self.distance_limit
        assert routeDijkstra.path[-1] == [G.geodata.nodes()[node]['x'], G.geodata.nodes()[node]['y']]
        
        # Verify that all elevation calculations are equal to 0.0
        assert routeDijkstra != None
        assert get_path_elevation(G, routeDijkstra.path) == 0.0

    def test_AStar_AA(self):
        # Initialize routes with same source and destination
        #self.distance_limit = 0.0
        self.InitializeModel(1, 1, self.G)

        # All routes found
        routeAStar = self.aStar.search()

        G = self.geoDataModel

        # Verify that each route is valid
        node = self.geoDataModel.dest
        assert routeAStar != None
        assert routeAStar.length <= self.distance_limit
        assert routeAStar.path[-1] == [G.geodata.nodes()[node]['x'], G.geodata.nodes()[node]['y']]
        
        # Verify that all elevation calculations are equal to 0.0
        assert routeAStar != None
        assert get_path_elevation(G, routeAStar.path) == 0.0

    def test_shortest_AA(self):
        #self.distance_limit = 0.0
        self.InitializeModel(1, 1, self.G)

        routeShortest = self.shortest.search()

        G = self.geoDataModel

        node = self.geoDataModel.dest
        assert routeShortest != None
        assert routeShortest.length <= self.distance_limit
        assert routeShortest.path[-1] == [G.geodata.nodes()[node]['x'], G.geodata.nodes()[node]['y']]
        
        # Verify that all elevation calculations are equal to 0.0
        assert routeShortest != None
        assert get_path_elevation(G, routeShortest.path) == 0.0

    # Expect path to be empty if nodes are the same or close
    def test_genetic_AA(self):
        #self.distance_limit = 0.0
        self.InitializeModel(1, 1, self.G)

        routeGenetic = self.genetic.cal_result()

        G = self.geoDataModel

        node = self.geoDataModel.dest
        assert routeGenetic != None
        assert routeGenetic.length <= self.distance_limit
        assert len(routeGenetic.path) == 0
        
        # Verify that all elevation calculations are equal to 0.0
        assert routeGenetic != None
        assert get_path_elevation(G, routeGenetic.path) == 0.0


        
if __name__ == "__main__":
    unittest.main()