import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import neighbors
import json


def create_Graph(num):
    G = nx.Graph()
    for i in range(0, num):
        G.add_node(i)
    return G


def make_Connected_Excess(G):
    num = 0
    while not nx.is_connected(G):
        nodes = random.sample(G.nodes, 2)
        if not G.has_edge(nodes[0], nodes[1]):
            G.add_edge(nodes[0], nodes[1])
            num += 1

    iters = num*1.5
    while num < iters:
        nodes = random.sample(G.nodes, 2)
        if not G.has_edge(nodes[0], nodes[1]):
            G.add_edge(nodes[0], nodes[1])
            num += 1

    return num


def propagateMsg(G):
    message_Source = random.sample(G.nodes, 1)[0]
    received = set([message_Source])
    already_Sent = set([])
    msgs_sent = 0
    while(len(received) < len(G.nodes)):
        for r in received.copy():
            if (True):
                already_Sent.add(r)
                for n in G.neighbors(r):
                    received.add(n)
                    msgs_sent += 1
    return msgs_sent


nodes = range(1, 156, 5)
results = {}

for n in nodes:
    messageCountResults = []
    linkCountResults = []
    diameterResults = []
    neighborsResults = []
    for _ in range(40):
        G = create_Graph(n)
        N = make_Connected_Excess(G)
        linkCountResults.append(N)
        neighborCountlist = [len(list(G.neighbors(r))) for r in G.nodes]
        neighborsResults.append(sum(neighborCountlist)/len(neighborCountlist))
        diameterResults.append(nx.algorithms.distance_measures.diameter(G))

        for _ in range(1000):
            msgs_sent = propagateMsg(G)
            messageCountResults.append(msgs_sent)

    neighborCountlist = [len(list(G.neighbors(r))) for r in G.nodes]
    results[n] = {
        'avgLinks': sum(linkCountResults)/len(linkCountResults),
        'avgDiameter': sum(diameterResults)/len(diameterResults),
        'avgMsgsSent': sum(messageCountResults)/len(messageCountResults),
        'avgNeighbors': sum(neighborCountlist)/len(neighborCountlist)
    }

################################
# Result Exporting
################################

with open('results/results.json', 'w') as f:
    json.dump(results, f)

edgesArray = [n['avgLinks'] for n in results.values()]
plt.xlabel("Number of Nodes")
plt.ylabel("Average Number of Edges Inserted")
plt.axis([min(nodes), max(nodes), min(edgesArray), max(edgesArray)])
plt.plot(nodes, edgesArray)
plt.savefig('results/edges.png')

diameterArray = [n['avgDiameter'] for n in results.values()]
plt.xlabel("Number of Nodes")
plt.ylabel("Average Diameter")
plt.axis([min(nodes), max(nodes), min(diameterArray), max(diameterArray)])
plt.plot(nodes, diameterArray)
plt.savefig('results/diameter.png')

neighborsArray = [n['avgNeighbors'] for n in results.values()]
plt.xlabel("Number of Nodes")
plt.ylabel("Average Number of neighbors")
plt.axis([min(nodes), max(nodes), min(neighborsArray), max(neighborsArray)])
plt.plot(nodes, neighborsArray)
plt.savefig('results/neighbors.png')

avgMsgsArray = [n['avgMsgsSent'] for n in results.values()]
plt.xlabel("Number of Nodes")
plt.ylabel("Average Number of messages sent")
plt.axis([min(nodes), max(nodes), min(avgMsgsArray), max(avgMsgsArray)])
plt.plot(nodes, avgMsgsArray)
plt.savefig('results/msgs.png')
