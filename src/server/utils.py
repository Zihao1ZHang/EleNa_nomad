def get_length(G, start, end):
    return G.edges[start, end, 0]['length']


def get_path_length(G, node_list):
    length = 0
    for i in range(len(node_list) - 1):
        length += get_length(G, node_list[i], node_list[i + 1])
    return length


def get_path_elevation(G, node_list):
    total_elevation = 0
    for i in range(len(node_list) - 1):
        curr_elevation = get_elevation_gain(G, node_list[i], node_list[i + 1])
        if curr_elevation > 0:
            total_elevation += curr_elevation
    return total_elevation


def get_elevation_gain(G, start, end):
    if start == end:
        return 0
    return G.nodes[start]['elevation'] - G.nodes[end]['elevation']
