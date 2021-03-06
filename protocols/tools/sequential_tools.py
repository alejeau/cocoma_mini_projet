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


def allocation_cost(allocation: [int], utilities: {(int, int): int}) -> int:
    if len(allocation) == 1:
        return 0
    else:
        free_nodes = copy.deepcopy(allocation)
        nodes = [free_nodes.pop(0)]
        total_cost = 0
        while free_nodes:
            min_cost = max(utilities.values())
            best_node = None
            for node in nodes:
                for free_node in free_nodes:
                    cost = utilities[(node, free_node)]
                    if cost <= min_cost:
                        min_cost = cost
                        best_node = free_node

            idx = free_nodes.index(best_node)
            nodes.append(free_nodes.pop(idx))
            total_cost += min_cost
        return total_cost


def envy_freeness(allocations: {str: [int]}, tour_costs: {str: [int]}, utilities: {(int, int): int}) -> {int: [(int, [int], int)]}:
    """

    :param allocations:
    :param tour_costs:
    :param utilities:
    :return:
        {int: [(int, [int], int)]} a dictionary formed as follow : {agent: [(agent's allocation, allocation, score)]}
    """
    envious_agents = {}

    for agent in allocations.keys():
        better_allocations = []
        utility = sum(tour_costs[agent])
        agent_score = utility
        for other in allocations.keys():
            if agent != other:
                allocation = allocations[other]
                score = allocation_cost(allocation, utilities)
                if score < agent_score:
                    better_allocations.append((other, allocation, score))
            if len(better_allocations) > 0:
                envious_agents.update({agent: better_allocations})

    return envious_agents
