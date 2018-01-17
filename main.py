#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
import networkx as nx
from Archivist import Archivist

max_weight = 10
log = Archivist()
log.open_file('log.txt')


def generate_sites(n: int, m: int):
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
def sequential_auctions(agents: [int], sites: nx.Graph) -> {int: [int]}:
    res = {}
    free_nodes = list(sites.nodes())

    # init agents location
    for a in agents:
        s_len = len(free_nodes)
        idx = random.randint(0, s_len-1)
        node = free_nodes.pop(idx)
        res.update({a: [node]})

    weight = max_weight
    while free_nodes:
        # for each agent, check the neighbours of the owned nodes, and bid on the one with the smallest weight
        log.log('\nfree_nodes: ' + str(free_nodes))
        auctions = {}
        for a in agents:
            nodes = res[a]
            best_node = None
            for node in nodes:
                neighbours = sites.neighbors(node)
                for neighbour in neighbours:
                    log.log('neighbour: ' + str(neighbour) + ', free nodes: ' + str(free_nodes))
                    if neighbour in free_nodes:
                        tmp_weight = sites[node][neighbour]['weight']
                        if tmp_weight < weight:
                            weight = tmp_weight
                            best_node = neighbour

            # """ ****************************************************************** """
            # """ ****************************************************************** """
            # """ ****************************************************************** """
            # # in case of a node without neighbours
            # # the algo crashes
            # # check the form of the graph
            # # and solve that shit
            # """ ****************************************************************** """
            # """ ****************************************************************** """
            # """ ****************************************************************** """
            #
            # if best_node is None and len(free_nodes) == 1:
            #     return res

            auctions.update({a: (weight, best_node)})

            # get the winners that bid on the smallest weight
            min_weights = max_weight
            winners = []
            for k in auctions.keys():
                w = auctions[k][0]
                if w <= min_weights:
                    if w < min_weights:
                        winners = []
                    min_weights = w
                    winners.append((k, auctions[k][1]))

            log.log('winners: ' + str(winners))
            # elect one winner between them all
            win_len = len(winners)
            if win_len == 1:
                winner = winners[0]
            else:
                winner = winners[random.randint(0, win_len-1)]

            # update the result list
            log.log('winner: ' + str(winner))
            agent = winner[0]
            node = winner[1]
            winner_nodes = res[agent]
            winner_nodes.append(node)
            res.update({agent: winner_nodes})
            # remove the won node from the list of free nodes

            log.log('free nodes: ' + str(free_nodes))
            free_nodes.remove(node)
            log.log('free nodes: ' + str(free_nodes))
            log.log('restart while loop')
    return res


def aff_graph(g: nx.Graph):
    nodes = list(g.nodes())
    edges = g.edges()
    str('nodes:')
    for n in nodes:
        log.log('n: ' + str(n))

    str('edges:')
    for e in edges:
        log.log('e: ' + str(e))

    str('weights:')
    for e in edges:
        x = e[0]
        y = e[1]
        log.log('g[' + str(x) + '][' + str(y) + '][weight]: ' + str(g[x][y]['weight']))


vertex = 7
g = generate_sites(vertex, 2*vertex-2)

while not nx.is_connected(g):
    g = generate_sites(vertex, 2*vertex-2)
# aff_graph(g)
# nx.draw(g)

agents = [0, 1]
results = sequential_auctions(agents, g)
log.log('results' + str(results))

log.close()
