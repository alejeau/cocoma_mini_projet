#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
import networkx as nx


max_weight = 10


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
    # nodes = list(sites.nodes())
    free_nodes = list(sites.nodes())

    # init agents location
    for a in agents:
        s_len = len(free_nodes)
        idx = random.randint(0, s_len-1)

        node = free_nodes.pop(idx)
        res.update({a: [node]})

    weight = max_weight
    while len(free_nodes) != 0:
        # for each agent, check the neighbours of the owned nodes, and bid on the one with the smallest weight
        print('\nfree_nodes: ' + str(free_nodes))
        for a in agents:
            auctions = {}
            nodes = res[a]
            best_node = None
            for node in nodes:
                neighbours = sites.neighbors(node)
                for neighbour in neighbours:
                    if neighbour in free_nodes:
                        tmp_weight = sites[node][neighbour]['weight']
                        if tmp_weight < max_weight:
                            weight = tmp_weight
                            best_node = neighbour

            """ ****************************************************************** """
            """ ****************************************************************** """
            """ ****************************************************************** """
            # in case of a node without neighbours
            # the algo crashes
            # check the form of the graph
            # and solve that shit
            """ ****************************************************************** """
            """ ****************************************************************** """
            """ ****************************************************************** """

            if best_node is None and len(free_nodes) == 1:
                return res

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

            print('winners: ' + str(winners))
            # elect one winner between them all
            win_len = len(winners)
            if win_len == 1:
                winner = winners[0]
            else:
                winner = winners[random.randint(0, win_len-1)]

            # update the result list
            print('winner: ' + str(winner))
            winner_nodes = res[winner[0]]
            winner_nodes.append(winner[1])
            print('winner[0]: ' + str(winner[0]))
            res.update({winner[0]: winner_nodes})
            # remove the won node from the list of free nodes
            free_nodes.remove(winner[1])

    return res


vertex = 7
g = generate_sites(vertex, 2*vertex-2)
results = sequential_auctions([0, 1], g)
print('results' + str(results))
