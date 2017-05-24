import networkx as nx
from collections import defaultdict
from path import Path


def get_routing_matrix(g):
    rm = defaultdict(defaultdict)
    sp = nx.all_pairs_shortest_path(g)

    for s in sp:
        for t in sp[s]:

            if s == t:
                continue

            p = Path(g, sp[s][t])
            rm[s][t] = [p]

    return rm


