import random
from topologies.connected_watts_strogatz_topology import get_topology
from traffic.zipf_traffic_matrix import get_traffic_matrix
#from routing.shortest_path_routing import get_routing_matrix
from routing.k_shortest_paths_routing import get_routing_matrix

from flow_solvers.sor import compute_sor

seed = 42
num_nodes = 10
edge_p = 0.1
k_nearest_neighbors = 2
connected_tries = 100

good_zipf_param = 1.6

random.seed(seed)

# Topology
# Get a random graph
g = get_topology(num_nodes, k_nearest_neighbors, edge_p, connected_tries, seed)

# Target
# Select a random target node
t = random.choice(list(g.nodes()))

# Traffic Matrices
# 'Good' traffic which normally flows between the a pair fo ASes
good_tm = get_traffic_matrix(g, good_zipf_param, num_nodes)

# 'Bad' traffic which is due to DDoS traffic being sent to the target node

# Routing
# The total offered load is then 'routed' via the underlying graph from sources to destinations
rm = get_routing_matrix(g)

compute_sor(g, good_tm, rm)

# Filtering
# Placing a filter at a node implies that it no longer routes the bad traffic
# We try two filtering strategies for placing k filters:
# Place the filters at top k nodes with highest degree
# Place the filters at top k nodes with highest bad traffic load

# Cumulative Delay
# After routing and filtering, the flow on edge is computed.
# This flow can then be used to compute the cumulative network delay experienced by everyone by using a delay model

