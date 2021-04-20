import os
import random
import networkx as nx
import matplotlib.pyplot as plt
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
    # 10 unsuccessfull tries to insert and edge break the cycle, it may not be possible to add such edge
    counter = 0
    while num < iters:
        counter += 1
        nodes = random.sample(G.nodes, 2)
        if not G.has_edge(nodes[0], nodes[1]):
            G.add_edge(nodes[0], nodes[1])
            num += 1
            counter = 0
        if counter == 10:
            break

    return num


def propagateMsg(G, broadcastfraction):
    message_Source = random.sample(G.nodes, 1)[0]
    received = set([message_Source])
    already_Sent = set([])
    msgs_sent = 0
    while(len(received) < len(G.nodes)):
        prevMsgSent = msgs_sent
        for r in received.copy():
            if (r not in already_Sent):
                already_Sent.add(r)
                for n in random.sample(list(G.neighbors(r)), int(len(list(G.neighbors(r)))*broadcastfraction)):
                    received.add(n)
                    msgs_sent += 1
        if(msgs_sent == prevMsgSent):
            return msgs_sent, len(received)

    return msgs_sent, len(received)


nodes = range(1, 156, 5)
broadcastfractions = [1, 0.8, 0.6, 0.4, 0.2]
graphToGenerate = 40
messagesToSend = 1000
broadcastfraction = 1
results = {}

for broadcastfraction in broadcastfractions:
    for n in nodes:
        receivedCountResults = []
        messageCountResults = []
        linkCountResults = []
        diameterResults = []
        neighborsResults = []
        # Generate Graphs for each node count
        for _ in range(graphToGenerate):
            G = create_Graph(n)
            N = make_Connected_Excess(G)
            linkCountResults.append(N)
            neighborCountlist = [len(list(G.neighbors(r))) for r in G.nodes]
            neighborsResults.append(
                sum(neighborCountlist)/len(neighborCountlist))
            diameterResults.append(nx.algorithms.distance_measures.diameter(G))
            # For each graph randomly propage messages from random sources
            for _ in range(messagesToSend):
                msgs_sent, len_received = propagateMsg(G, broadcastfraction)
                receivedCountResults.append(len_received)
                messageCountResults.append(msgs_sent)

        neighborCountlist = [len(list(G.neighbors(r))) for r in G.nodes]
        results[n] = {
            'avgLinks': sum(linkCountResults)/len(linkCountResults),
            'avgDiameter': sum(diameterResults)/len(diameterResults),
            'avgMsgsSent': sum(messageCountResults)/len(messageCountResults),
            'avgNeighbors': sum(neighborCountlist)/len(neighborCountlist),
            'percentReceived': (sum(receivedCountResults)/len(receivedCountResults))/n
        }

    ################################
    # Result Exporting
    ################################

    try:
        os.mkdir(f'results{broadcastfraction}')
    except Exception as e:
        print("Directory exists: ", e)

    with open(f'results{broadcastfraction}/results.json', 'w') as f:
        json.dump(results, f)

    edgesArray = [n['avgLinks'] for n in results.values()]
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Number of Edges Inserted")
    plt.axis([min(nodes), max(nodes), min(edgesArray), max(edgesArray)])
    plt.plot(nodes, edgesArray)
    plt.savefig(f'results{broadcastfraction}/edges.png')
    plt.clf()

    diameterArray = [n['avgDiameter'] for n in results.values()]
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Diameter")
    plt.axis([min(nodes), max(nodes), min(diameterArray), max(diameterArray)])
    plt.plot(nodes, diameterArray)
    plt.savefig(f'results{broadcastfraction}/diameter.png')
    plt.clf()

    neighborsArray = [n['avgNeighbors'] for n in results.values()]
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Number of neighbors")
    plt.axis([min(nodes), max(nodes), min(neighborsArray), max(neighborsArray)])
    plt.plot(nodes, neighborsArray)
    plt.savefig(f'results{broadcastfraction}/neighbors.png')
    plt.clf()

    avgMsgsArray = [n['avgMsgsSent'] for n in results.values()]
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Number of messages sent")
    plt.axis([min(nodes), max(nodes), min(avgMsgsArray), max(avgMsgsArray)])
    plt.plot(nodes, avgMsgsArray)
    plt.savefig(f'results{broadcastfraction}/msgs.png')
    plt.clf()

    percentReceivedArray = [n['percentReceived'] for n in results.values()]
    plt.xlabel("Number of Nodes")
    plt.ylabel("Percent of nodes that received the message")
    plt.axis([min(nodes), max(nodes), min(
        percentReceivedArray)-0.05, max(percentReceivedArray)+0.05])
    plt.plot(nodes, percentReceivedArray)
    plt.savefig(f'results{broadcastfraction}/percentReceived.png')
    plt.clf()
