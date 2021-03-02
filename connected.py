import random
import networkx as nx
import matplotlib.pyplot as plt


def create_Graph(num):
    G = nx.Graph()
    for i in range(0, num):
        G.add_node(i)
    return G


def make_Connected(G):
    num = 0
    while not nx.is_connected(G):
        nodes = random.sample(G.nodes, 2)
        if not G.has_edge(nodes[0], nodes[1]):
            G.add_edge(nodes[0], nodes[1])
            num = num + 1
    return num


nodes = [x for x in range(1, 101, 5)]
results = []
for numNodes in nodes:
    print(numNodes)
    edges = []
    for i in range(0, 20000):
        G = create_Graph(numNodes)
        N = make_Connected(G)
        edges.append(N)
    results.append(sum(edges)/len(edges))

plt.xlabel("Number of Nodes")
plt.ylabel("Average Number of Edges Inserted")
plt.axis([min(nodes), max(nodes), min(results), max(results)])
plt.plot(nodes, results)
plt.savefig('file.png')
plt.savefig('file.pdf')
plt.savefig('file.svg')
