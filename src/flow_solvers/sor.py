import numpy as np
from itertools import repeat
from scipy.optimize import minimize


# The function is expressed with two set of variables
# x_j variables represent the total flow on each link j
# y_p variables represent the flow assigned to a given path p

# The required inputs are:
# The set of links in the graph, each link corresponds to the index j
# The set of paths between a source/destination pair (P_i), each pair is denoted by the index i
## Each path is expressed as a subset of links in the graph
# The offered load between a source/destination pair (X_i), each pair is denoted by the index i


def compute_sor(g, tm, rm):

    # Get A: The list of all the edges
    # edge_paths is a list of all the routing paths that traverse a given edge

    cntr = 0
    A = list()
    for e in g.edges():
        g[e[0]][e[1]]["edge_paths"] = []
        g[e[0]][e[1]]["j"] = cntr
        cntr += 1
        A.append(e)

    # Get W: The list of triples: s, t and flow quantity from s to t
    W = list()
    for s in g.nodes():
        for t in g.nodes():
            if s != t:
                W.append((s, t, tm[s][t]))

    # Get P: The list of all the paths in the routing instance. Each path is a list of edges
    P = list()
    for s in g.nodes():
        for t in g.nodes():
            if s != t:
                for path in rm[s][t]:
                    path.p = cntr
                    cntr += 1
                    P.append(path)

                    for edge in path.edge_list:
                        g[edge[0]][edge[1]]["edge_paths"].append(path)

    def func(x, sign=1.0):
        func_val = sign
        sum = 0

        for j in range(len(A)):
            sum += x[j] * x[j] * x[j]

        func_val *= sum

        return float(func_val)

    def func_deriv(x, sign=1.0):
        deriv_list = list()

        for j in range(len(A)):
            term_deriv = 3 * x[j] * x[j]
            deriv_list.append(sign * term_deriv)

        for p in range(len(P)):
            deriv_list.append(0)

        return np.array(deriv_list)

    cons_list = []

    def get_total_edge_flow_constraints():
        for j in range(len(A)):

            def fun(x, edge, j):
                sum = 0

                paths = g[edge[0]][edge[1]]["edge_paths"]

                for path in paths:
                    sum += x[path.p]

                return np.array([sum - x[j]])

            def jac(x, edge, j):
                jac_array = []

                for q in range(len(A) + len(P)):

                    if q == j:
                        jac_array.append(-1.0)
                    else:
                        found_variable_use_in_paths = False
                        paths = g[edge[0]][edge[1]]["edge_paths"]

                        for path in paths:
                            if path.p == q:
                                found_variable_use_in_paths = True
                                break

                        if found_variable_use_in_paths:
                            jac_array.append(1.0)
                        else:
                            jac_array.append(0)

                return np.array(jac_array)

            con = {'type': 'eq',
                   'fun': fun,
                   'jac': jac,
                   'args': (A[j], j)}

            cons_list.append(con)

    def get_total_src_dst_pair_flow_constraints():
        for i in range(len(W)):

            def fun(x, s, t, X_i):
                sum = 0

                # Sum flow over all paths
                for path in rm[s][t]:
                    sum += x[path.p]

                return np.array([sum - X_i])

            def jac(x, s, t, X_i):
                jac_array = []
                for q in range(len(A) + len(P)):
                    found_variable_use_in_paths = False
                    for path in rm[s][t]:
                        if path.p == q:
                            found_variable_use_in_paths = True
                            break

                    if found_variable_use_in_paths:
                        jac_array.append(1.0)
                    else:
                        jac_array.append(0)

                return np.array(jac_array)

            con = {'type': 'eq',
                   'fun': fun,
                   'jac': jac,
                   'args': W[i]}

            cons_list.append(con)

    def get_positive_value_bounds():
        bnds = []
        for q in range(len(A) + len(P)):
            bnds.append((0, None))
        return bnds

    get_total_edge_flow_constraints()
    get_total_src_dst_pair_flow_constraints()

    cons_tuple = tuple(cons_list)

    initial_guess = list(repeat(0.5, len(A) + len(P)))

    res = minimize(func,
                   initial_guess,
                   args=(-1.0,),
                   jac=func_deriv,
                   constraints=cons_tuple,
                   method='SLSQP',
                   bounds=get_positive_value_bounds(),
                   options={'disp': True})

    print(res.x)

    for e in g.edges():
        g[e[0]][e[1]]["edge_flow"] = res.x[g[e[0]][e[1]]["j"]]

    for path in P:
        path.assigned_flow = res.x[path.p]

