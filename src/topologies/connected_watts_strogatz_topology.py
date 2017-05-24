import networkx as nx
#import matplotlib.pyplot as plt


# def get_erdos_renyi_graph(num_nodes, edge_p, seed):
#     g = nx.erdos_renyi_graph(num_nodes, edge_p, seed)
#     return g


def get_topology(num_nodes, nearest_k, edge_p, tries, seed):
    g = nx.connected_watts_strogatz_graph(num_nodes, nearest_k, edge_p, tries, seed)
    #nx.draw_circular(g)
    #plt.show()
    return g
