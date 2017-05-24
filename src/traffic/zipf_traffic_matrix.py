import numpy as np
#import matplotlib.pyplot as plt
from scipy import special
from collections import defaultdict


def get_traffic_matrix(g, zipf_param, num_nodes):
    tm = defaultdict(defaultdict)
    for node in g.nodes():
        s = np.random.zipf(zipf_param, num_nodes)
        for i in range(len(s)):
            if i != node:
                tm[node][i] = s[i]
    return tm


def play():
    a = 2.0 # parameter
    s = np.random.zipf(a, 1000)
    # print max(s)
    # s = s * 1.0/max(s)
    count, bins, ignored = plt.hist(s[s < 50], 50, normed=True)
    x = np.arange(1., 50.)
    y = x**(-a) / special.zetac(a)
    plt.plot(x, y/max(y), linewidth=2, color='r')
    plt.show()

#play()
