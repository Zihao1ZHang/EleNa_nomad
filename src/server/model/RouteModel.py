class Route(object):
    """ The class store the data of the route

    Args:
        path (list of coordinates) : list contains coordinates, which each 
                        coordinate corresponds to a node in the node_list in the same order
        length (float) : the total length of the path
        elevation (float) : the total elevation gain of the path 
    """

    def __init__(self, path, length, elevation):
        self.path = path
        self.length = length
        self.elevation = elevation
