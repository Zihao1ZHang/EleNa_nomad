import osmnx as ox


class GeoData(object):
    def __init__(self, source, dest, key, G=None):
        G = ox.graph_from_bbox(north=max(source[1], dest[1])+0.01, south=min(
            source[1], dest[1])-0.01, east=max(source[0], dest[0])+0.01, west=min(source[0], dest[0])-0.01)
        G = ox.elevation.add_node_elevations_google(
            G, api_key=key)
        G = ox.elevation.add_edge_grades(G)
        self.geodata = G
        self.source = ox.nearest_nodes(G, source[0], source[1])
        self.dest = ox.nearest_nodes(G, dest[0], dest[1])
