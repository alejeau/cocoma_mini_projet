#!/usr/bin/python3
# -*-coding: utf-8 -*

import copy
import networkx as nx


def extract_utility_from_graph(g: nx.Graph) -> {(int, int): int}:
    nodes = g.nodes()
    utilities = {}
    for node1 in nodes:
        for node2 in nodes:
            if node1 != node2:
                utilities.update({(node1, node2): g[node1][node2]['weight']})

    return utilities


def sites_utility(g: nx.Graph):
    utility = {}
    t = nx.minimum_spanning_tree(g)
    edges = t.edges(data=True)

    for edge in edges:
        x = edge[0]
        y = edge[1]
        w = edge[2]['weight']
        utility.update({(x, y): w})

    return utility


def sites_utility_handmade(sites: nx.Graph):
    free_nodes = sorted(sites.nodes())
    nodes = [free_nodes.pop(0)]
    utility = {}
    while free_nodes:
        interesting_edges_by_weight = {}
        for node in nodes:
            neighbours = sites.neighbors(node)
            for neighbour in neighbours:
                if neighbour in free_nodes:
                    weight = sites[node][neighbour]['weight']
                    iebw = interesting_edges_by_weight.get(weight, [])
                    iebw.append((node, neighbour))
                    interesting_edges_by_weight.update({weight: iebw})

        min_weight = min(interesting_edges_by_weight.keys())
        edge = interesting_edges_by_weight[min_weight][0]
        utility.update({edge: min_weight})
        index = free_nodes.index(edge[1])
        nodes.append(free_nodes.pop(index))

    return utility


def utility_score(allocation: [int], utility: [int]) -> int:
    score = 0
    for a in allocation:
        score += utility[a]

    return score


"""
def egalitarian_social_welfare(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: [([int], int)]}:
    utility_scores = {}
    for agent in allocations.keys():
        score = utility_score(allocations[agent], utilities[agent])
        utility_scores.update({agent: score})

    print('utility_scores: ' + str(utility_scores))

    worst_score = max(utility_scores.values())
    print('worst_score: ' + str(worst_score))
    worst_off_agents = []
    for agent in utility_scores.keys():
        if utility_scores[agent] == worst_score:
            worst_off_agents.append(agent)

    wronged_agents = {}
    for woa in worst_off_agents:
        better_allocations = []
        utility = utilities[woa]
        for agent in allocations.keys():
            allocation = allocations[agent]
            score = utility_score(allocation, utility)
            if score < worst_score:
                better_allocations.append((agent, allocation, score))
        if len(better_allocations) > 0:
            wronged_agents.update({woa: better_allocations})

    return wronged_agents
"""


def proportional_fair_share(allocations: {str: [int]}, tour_costs: {str: [int]}, sites: nx.Graph) -> {str: [([int], int)]}:
    s_utility = sum(sites_utility(sites).values())
    pfs = {}
    agents = allocations.keys()
    number_of_agents = len(agents)
    share = s_utility / number_of_agents
    for agent in agents:
        tour_cost = tour_costs[agent]
        agent_utility = sum(tour_cost)
        prop = True if agent_utility <= share else False
        allocation = allocations[agent]
        pfs.update({agent: (share, allocation, prop)})

    return pfs


def envy_freeness(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: [([int], int)]}:
    envious_agents = {}

    # utility_scores = {}
    # for agent in allocations.keys():
    #     score = utility_score(allocations[agent], utilities[agent])
    #     utility_scores.update({agent: score})
    #
    # for agent in allocations.keys():
    #     better_allocations = []
    #     utility = utilities[agent]
    #     agent_score = utility_scores[agent]
    #     for other in allocations.keys():
    #         if agent != other:
    #             allocation = allocations[other]
    #             score = utility_score(allocation, utility)
    #             if score < agent_score:
    #                 better_allocations.append((agent, allocation, score))
    #         if len(better_allocations) > 0:
    #             envious_agents.update({agent: better_allocations})

    return envious_agents
