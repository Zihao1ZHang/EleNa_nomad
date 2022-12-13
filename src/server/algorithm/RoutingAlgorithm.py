from abc import ABC, abstractmethod


class RoutingAlgorithm(ABC):
    @abstractmethod
    def __init__(self, GeoData):
        pass

    @abstractmethod
    def search(self, precent, is_max):
        pass
