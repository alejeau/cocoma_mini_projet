#!/usr/bin/python3
# -*-coding: utf-8 -*

import copy
import networkx as nx

""" **************************************************************************************************************** """
""" **************************************************************************************************************** """
""" **************************************************************************************************************** """
"""                                       still somewhat bugged                                                      """
""" **************************************************************************************************************** """
""" **************************************************************************************************************** """
""" **************************************************************************************************************** """


def sequential_auctions_with_regret(agents: [int], sites: nx.Graph, positions: {}, free_sites: [int], max_weight):
    allocations = copy.deepcopy(positions)
    free_nodes = copy.deepcopy(free_sites)
    tour_costs = {agent: [0] for agent in agents}

    while free_nodes:
        # for each agent, check the neighbours of the owned nodes, and bid on the one with the smallest weight
        auctions = {}
        for agent in agents:
            agent_nodes = allocations[agent]
            interesting_couples = set()
            for node in agent_nodes:
                neighbours = sites.neighbors(node)
                for free_node in free_nodes:
                    if free_node in neighbours:
                        interesting_couples.add((node, free_node))

            interesting_couples = list(interesting_couples)
            # for each free_node, add the related protocols
            for ic in interesting_couples:
                node = ic[0]
                free_node = ic[1]
                weight = sites[node][free_node]['weight']
                auction = auctions.get(free_node, {})
                agent_found = False
                for k in auction.keys():
                    if agent == k:
                        agent_found = True
                        if weight < auction[k]:
                            auction[k] = weight
                            break
                if not agent_found:
                    auction.update({agent: weight})
                auctions.update({free_node: auction})

        regrets = {}
        for free_node in auctions.keys():
            auction_dict = auctions[free_node]
            if auction_dict:
                min_weight = max_weight + 1
                min_auction = ()
                for tmp_agent in auction_dict.keys():
                    tmp_weight = auction_dict[tmp_agent]
                    if tmp_weight < min_weight:
                        min_weight = tmp_weight
                        min_auction = (tmp_weight, tmp_agent)

                auction_dict.pop(min_auction[1])
                min_weight = max_weight + 1
                for tmp_agent in auction_dict.keys():
                    tmp_weight = auction_dict[tmp_agent]
                    if tmp_weight < min_weight:
                        min_weight = tmp_weight
                regret = min_weight - min_auction[0]
                agent = min_auction[1]
                regrets.update({free_node: (regret, agent)})

        node = None
        winner = None
        max_regret = -1
        for free_node in regrets.keys():
            regret = regrets[free_node][0]
            if regret > max_regret:
                max_regret = regret
                node = free_node
                winner = regrets[free_node][1]

        winner_nodes = allocations[winner]
        winner_nodes.append(node)
        allocations.update({winner: winner_nodes})
        tour_cost = tour_costs[agent]
        tour_cost.append(max_regret)
        tour_costs.update({agent: tour_cost})
        # remove the won node from the list of free nodes
        free_nodes.remove(node)

    return allocations, tour_costs
