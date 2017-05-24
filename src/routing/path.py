class Path(object):

    def __init__(self, g, node_list):
        self.g = g
        self.node_list = node_list
        self.edge_list = self.get_edge_list(node_list)
        self.p = None
        self.assigned_flow = None

    def get_edge_list(self, node_list):
        edge_list = []

        for i in range(0, len(node_list) - 1):
            edge_list.append((node_list[i], node_list[i+1]))

        return edge_list

    def __str__(self):
        return str(self.edge_list)

    def __repr__(self):
        return str(self.edge_list)
