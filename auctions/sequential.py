#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
import networkx as nx


# enchères séquentielles : protocole :
# chaque agent fait une offre pour le sommet de coût minimum pour chaque sommet contôllé par l'agent
# un commissaire octroi l'offre de coût minimum à l'agent qui l'a faite
# et on recommence jusqu'à que tous les sommets soient distribués
def sequential_auctions(agents: [int], sites: nx.Graph, max_weight):
    res = {}
    free_nodes = list(sites.nodes())

    # init agents location
    for a in agents:
        s_len = len(free_nodes)
        idx = random.randint(0, s_len - 1)
        node = free_nodes.pop(idx)
        res.update({a: [node]})

    while free_nodes:
        # for each agent, check the neighbours of the owned nodes, and bid on the one with the smallest weight
        auctions = {}
        for agent in agents:
            agent_nodes = res[agent]
            interesting_couples = set()
            for node in agent_nodes:
                neighbours = sites.neighbors(node)
                for free_node in free_nodes:
                    if free_node in neighbours:
                        interesting_couples.add((node, free_node))

            interesting_couples = list(interesting_couples)
            weight = max_weight + 1
            for ic in interesting_couples:
                a = ic[0]
                b = ic[1]
                tmp_weight = sites[a][b]['weight']
                if tmp_weight < weight:
                    weight = tmp_weight
                    auctions.update({agent: (a, b, weight)})

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

        # elect one winner between them all
        win_len = len(winners)
        if win_len == 1:
            winner = winners[0]
        else:
            winner = winners[random.randint(0, win_len - 1)]

        # update the result list
        agent = winner[0]
        node = winner[1]
        winner_nodes = res[agent]
        winner_nodes.append(node)
        res.update({agent: winner_nodes})
        # remove the won node from the list of free nodes
        free_nodes.remove(node)

    return res
