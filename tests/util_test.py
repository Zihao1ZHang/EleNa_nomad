from src.server.utils import *
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

import unittest
import pytest
import os
import sys


class TestUtil(unittest.TestCase):
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

    """ Test utils.py functions """

    def test_get_length(self):
        assert get_length(self.G, 1, 2) == 2.0
        assert get_length(self.G, 2, 3) == 2.0
        assert get_length(self.G, 1, 3) == 5.0

    def test_get_length_FAIL(self):
        with self.assertRaises(Exception) as context:
            get_length(self.G_disconnected, 1, 3)
            get_length(self.G_disconnected, 2, 3)

    def test_get_path_length(self):
        path1 = [1, 2, 3]
        path2 = [1, 3]
        path3 = [2, 3]
        path4 = [1, 2]
        assert get_path_length(self.G, path1) == 4.0
        assert get_path_length(self.G, path2) == 5.0
        assert get_path_length(self.G, path3) == 2.0
        assert get_path_length(self.G, path4) == 2.0

    def test_get_path_length_FAIL(self):
        path1 = [1, 3]
        path2 = [2, 3]
        path3 = [1, 2, 3]
        with self.assertRaises(Exception) as context:
            get_path_length(self.G_disconnected, None)
            get_path_length(self.G_disconnected, [])
            get_path_length(self.G_disconnected, path1)
            get_path_length(self.G_disconnected, path2)
            get_path_length(self.G_disconnected, path3)

    def test_get_elevation_gain(self):
        assert get_elevation_gain(self.G, 1, 2) == -10.0
        assert get_elevation_gain(self.G, 2, 3) == -10.0
        assert get_elevation_gain(self.G, 1, 3) == -20.0

    def test_get_elevation_gain_FAIL(self):
        with self.assertRaises(Exception) as context:
            get_elevation_gain(self.G_disconnected, 1, 3)
            get_elevation_gain(self.G_disconnected, 2, 3)

    def test_get_path_elevation(self):
        path1 = [1, 2, 3]
        path2 = [1, 3]
        path3 = [2, 3]
        path4 = [1, 2]
        assert get_path_elevation(self.G, path1) == 0.0
        assert get_path_elevation(self.G, path2) == 0.0
        assert get_path_elevation(self.G, path3) == 0.0
        assert get_path_elevation(self.G, path4) == 0.0

    def test_get_path_elevation_FAIL(self):
        path1 = [1, 3]
        path2 = [2, 3]
        path3 = [1, 2, 3]
        with self.assertRaises(Exception) as context:
            get_path_elevation(self.G_disconnected, None)
            get_path_elevation(self.G_disconnected, [])
            get_path_elevation(self.G_disconnected, path1)
            get_path_elevation(self.G_disconnected, path2)
            get_path_elevation(self.G_disconnected, path3)
