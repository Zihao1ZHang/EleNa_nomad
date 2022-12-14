from abc import ABC, abstractmethod


class RoutingAlgorithm(ABC):
    """
    Abstract class for routing algorithms

    This class provides a basic outline for implementing routing algorithms.
    Subclasses must implement the __init__ and search methods.
    """
    @abstractmethod
    def __init__(self, GeoData):
        pass

    @abstractmethod
    def search(self, precent, is_max):
        pass
