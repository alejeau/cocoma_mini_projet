#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
import networkx as nx
import matplotlib.pyplot as plt
from Archivist import Archivist

max_weight = 10
log = Archivist()
log.open_file('log.txt')


def generate_sites(n, m):
    g = nx.gnm_random_graph(n, m)
    for e in list(g.edges()):
        x = e[0]
        y = e[1]
        g[x][y]['weight'] = random.randint(1, max_weight)

    return g


# enchères séquentielles : protocole :
# chaque agent fait une offre pour le sommet de coût minimum pour chaque sommet contôllé par l'agent
# un commissaire octroi l'offre de coût minimum à l'agent qui l'a faite
# et on recommence jusqu'à que tous les sommets soient distribués
def sequential_auctions(agents, sites):
    res = {}
    free_nodes = list(sites.nodes())

    # init agents location
    for a in agents:
        s_len = len(free_nodes)
        idx = random.randint(0, s_len-1)
        node = free_nodes.pop(idx)
        res.update({a: [node]})
        
    print('free_nodes: ' + str(free_nodes))
    print('res: ' + str(res))

    while free_nodes:
        # for each agent, check the neighbours of the owned nodes, and bid on the one with the smallest weight
        print('\nfree_nodes: ' + str(free_nodes))
        auctions = {}
        for agent in agents:
            agent_nodes = res[agent]
            interesting_couples = set()
            for node in agent_nodes:
                neighbours = sites.neighbors(node)
#                for neighbour in neighbours:
#                    neighbouring_nodes.add(neighbour)
                for free_node in free_nodes:
                    if free_node in neighbours:
                        interesting_couples.add((node, free_node))
            
            interesting_couples = list(interesting_couples)
            print('interesting_couples: ' + str(interesting_couples))
            
            weight = max_weight + 1
            for ic in interesting_couples:
                a = ic[0]
                b = ic[1]
                tmp_weight = sites[a][b]['weight']
                if tmp_weight < weight:
                    weight = tmp_weight
                    auctions.update({agent: (a, b, weight)})
         
            print('auctions: ' + str(auctions))

        # get the winners that bid on the smallest weight
        min_weight = max_weight
        winners = []
        for k in auctions.keys():
            w = auctions[k][2]
            if w <= min_weight:
                if w < min_weight:
                    winners = []
                min_weight = w
                winners.append((k, auctions[k][1]))

        print('winners: ' + str(winners))
        # elect one winner between them all
        win_len = len(winners)
        winner = None
        if win_len == 1:
            winner = winners[0]
        else:
            winner = winners[random.randint(0, win_len-1)]

        # update the result list
        print('winner: ' + str(winner))
        agent = winner[0]
        node = winner[1]
        winner_nodes = res[agent]
        winner_nodes.append(node)
        res.update({agent: winner_nodes})
        # remove the won node from the list of free nodes
        
        print('free nodes: ' + str(free_nodes))
        free_nodes.remove(node)
        print('free nodes: ' + str(free_nodes))
        print('restart while loop')
    return res


def aff_graph(g):
    nodes = list(g.nodes())
    edges = g.edges()
    str('nodes:')
    for n in nodes:
        print('n: ' + str(n))

    str('edges:')
    for e in edges:
        print('e: ' + str(e))

    str('weights:')
    for e in edges:
        x = e[0]
        y = e[1]
        print('g[' + str(x) + '][' + str(y) + '][weight]: ' + str(g[x][y]['weight']))


vertex = 7
g = generate_sites(vertex, 2*vertex-2)

while not nx.is_connected(g):
    g = generate_sites(vertex, 2*vertex-2)
#aff_graph(g)
#nx.draw(g)
#plt.show()

agents = [0, 1]
results = sequential_auctions(agents, g)
print('results' + str(results))

log.close()
