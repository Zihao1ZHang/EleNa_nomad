def get_length(G, start, end):
    return G.edges[start, end, 0]['length']


def get_path_length(G, node_list):
    length = 0

    for i in range(len(node_list) - 1):
        length += get_length(G, node_list[i], node_list[i + 1])

    return length
