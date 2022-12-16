from src.server.algorithm.Shortest_algorithm import Shortest
from src.server.algorithm.Dijkstra_algorithm import Dijkstra
from src.server.algorithm.Astar_algorithm import Astar
import unittest
import osmnx as ox
from src.server.model.keys import google_elevation_api_key
from src.server.model.GeoDataModel import GeoData


class TestGoogleAPI(unittest.TestCase):
    
    def test_api(self):
        """ This is method to test whether google map api works correctly
        """
        x = [-72.50288753707943, 42.37470719043611]
        y = [-72.49943285186812, 42.369824609833614]
        assert GeoData(x, y, google_elevation_api_key)
