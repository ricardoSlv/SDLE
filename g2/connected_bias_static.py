from functools import reduce
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

nodes = [x for x in range(1, 101, 5)]


def create_Graph(num):
    G = nx.Graph()
    for i in range(0, num):
        G.add_node(i)
    return G


def make_Connected(G):
    num = 0
    connects = [1 for _ in G.nodes]
    while not nx.is_connected(G):

        nodes = random.choices(list(G.nodes), weights=connects, k=2)
        if not G.has_edge(nodes[0], nodes[1]):
            connects[nodes[0]] += 1
            connects[nodes[1]] += 1
            G.add_edge(nodes[0], nodes[1])
            num = num + 1
    print(connects)
    return num, connects


results = []
for numNodes in nodes:
    print(numNodes)
    edges = []
    cons = []
    for i in range(0, 30):
        G = create_Graph(numNodes)
        N, con = make_Connected(G)
        edges.append(N)
        cons.append(sorted(con))
    results.append(sum(edges)/len(edges))

    normalizedEdges = list(map(lambda sum: int(sum/30),
                               reduce(lambda x, y: np.add(x, y),
                                      list(map(lambda con: list(map(lambda val: val-1, con)),
                                               cons)))))
    # print(normalizedEdges)
    values = []
    occurrences = []
    for i, x in enumerate(normalizedEdges[:-1]):
        if x == normalizedEdges[i+1]:
            if(len(occurrences) > 0):
                occurrences[-1] += 1
            else:
                values.append(x)
                occurrences = [1]
        else:
            values.append(x)
            occurrences.append(1)
    # print(values)
    # print(occurrences)
    plt.clf()
    plt.bar(values, occurrences, color='blue', width=0.4)
    plt.savefig(f'static_dist_{numNodes}_nodes.png')

plt.clf()
plt.xlabel("Number of Nodes")
plt.ylabel("Average Number of Edges Inserted")
plt.axis([min(nodes), max(nodes), min(results), max(results)])
plt.plot(nodes, results)
plt.savefig(f'static.png')
# plt.savefig('file.pdf')
# plt.savefig('file.svg')
