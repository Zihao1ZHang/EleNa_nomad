import osmnx as ox
# from googleapiclient.errors import HttpError


class GeoData(object):
    """ The GeoData class is used to request and store the map data for a given search area.

    Args:
        source ((float, float)) : the coordinate of the starting point
        dest((float, float)) : the coordinate of the destination point
        key (String) : the API key used to access the map data.
        G (networkx.MultiDiGraph) : MutliDiGraph object that contains the 
            map data in the searching area
    """

    def __init__(self, source, dest, key, G=None, test=False):
        """ The __init__ method initializes a new GeoData object by setting the geodata attribute
            to the G argument, or to a new MultiDiGraph object created using the bounding box 
            defined by the source and dest coordinates.
        """
        self.test = test
        if G == None:
            # try:
            G = ox.graph_from_bbox(north=max(source[1], dest[1])+0.01, south=min(
                source[1], dest[1])-0.01, east=max(source[0], dest[0])+0.01, west=min(source[0], dest[0])-0.01)
            G = ox.elevation.add_node_elevations_google(
                G, api_key=key)
            G = ox.elevation.add_edge_grades(G)
            # except HttpError as error:
            #     raise Exception("Invalid API key" + str(error))
            
        self.geodata = G
        if test == True:
            self.source = source
            self.dest = dest
        else:
            self.source = ox.nearest_nodes(G, source[0], source[1])
            self.dest = ox.nearest_nodes(G, dest[0], dest[1])
