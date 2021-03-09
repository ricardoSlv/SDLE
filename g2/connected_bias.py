import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce

nodes = 100
weight = 1


def create_Graph(num):
    G = nx.Graph()
    for i in range(0, num):
        G.add_node(i)
    return G


def make_connected_size(G):
    connects = []
    for i in range(nodes):
        G.add_node(i)
        connects.append(1)
        while not nx.is_connected(G):
            node = random.choices(list(G.nodes), weights=connects, k=1)[0]
            if not G.has_edge(node, i):
                connects[node] += weight
                connects[i] += weight
                G.add_edge(node, i)
    return connects


results = []
for i in range(0, 30):
    G = create_Graph(0)
    connects = make_connected_size(G)
    results.append(sorted(connects, reverse=True))


normalizedEdges = list(map(lambda sum: sum/30, reduce(lambda x, y: np.add(x, y), list(
    map(lambda con: list(map(lambda val: val-1, con)), results)))))

values = []
occurrences = []
for i, x in enumerate(list(map(lambda x: int(x), (normalizedEdges[:-1])))):
    if x == normalizedEdges[i+1]:
        occurrences[-1] += 1
    else:
        values.append(x)
        occurrences.append(1)

print(values)
print(occurrences)
# plt.xlabel("Number of Nodes")
# plt.ylabel("Average Number of Edges Inserted")
# plt.axis([0, 100, 0, 1000])

#plt.plot(values, occurrences)
plt.bar(values, occurrences, color='blue', width=0.4)
plt.savefig(f'distribution.png')
# plt.savefig('file.svg')
# plt.savefig('file.pdf')
