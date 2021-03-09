import random
import networkx as nx
import matplotlib.pyplot as plt

nodes = [x for x in range(1, 101, 5)]
weight = 0


def create_Graph(num):
    G = nx.Graph()
    for i in range(0, num):
        G.add_node(i)
    return G


def make_Connected(G):
    num = 0
    connects = [1 for _ in G.nodes]
    while not nx.is_connected(G):

        nodes = random.choices({i: x for i, x in enumerate(
            G.nodes)}, weights=connects, cum_weights=None, k=2)
        if not G.has_edge(nodes[0], nodes[1]):
            connects[nodes[0]] += weight
            connects[nodes[1]] += weight
            G.add_edge(nodes[0], nodes[1])
            num = num + 1
    return num


while(weight < 10):
    results = []
    for numNodes in nodes:
        print(numNodes)
        edges = []
        for i in range(0, 30):
            G = create_Graph(numNodes)
            N = make_Connected(G)
            edges.append(N)
        results.append(sum(edges)/len(edges))

    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Number of Edges Inserted")
    plt.axis([min(nodes), max(nodes), min(results), max(results)])
    plt.plot(nodes, results)
    plt.savefig(f'weight_{weight}.png')
    weight += 0.5
# plt.savefig('file.pdf')
# plt.savefig('file.svg')
