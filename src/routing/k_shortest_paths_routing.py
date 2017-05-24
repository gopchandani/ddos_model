import networkx as nx
from itertools import islice
from collections import defaultdict
from routing.path import Path


def get_routing_matrix(g, k=2):
    rm = defaultdict(defaultdict)

    for s in g.nodes():
        for t in g.nodes():

            if s == t:
                continue

            rm[s][t] = []

            for path_nodes in islice(nx.shortest_simple_paths(g, s, t), k):
                p = Path(g, path_nodes)
                rm[s][t].append(p)

    return rm
