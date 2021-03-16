import random
import networkx as nx
import matplotlib.pyplot as plt


def create_Graph(num):
    G = nx.Graph()
    for i in range(0, num):
        G.add_node(i)
    return G


def make_Connected(G):
    connects = [1 for _ in G.nodes]
    while not nx.is_connected(G):

        nodes = random.choices(list(G.nodes), weights=connects, k=2)
        if not G.has_edge(nodes[0], nodes[1]):
            connects[nodes[0]] += 1
            connects[nodes[1]] += 1
            G.add_edge(nodes[0], nodes[1])
    return connects


numNodes = 100
G = create_Graph(numNodes)
connects = make_Connected(G)

connects = list(map(lambda val: val-1, connects))

plt.bar([x for x in range(numNodes)], sorted(
    connects, reverse=True), color='blue', width=0.4)
plt.savefig(f'static_dists_pics/{numNodes}_nodes.png')
