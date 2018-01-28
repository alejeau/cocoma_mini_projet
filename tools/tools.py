#!/usr/bin/python3
# -*-coding: utf-8 -*

import numpy as np
import random as rand
import networkx as nx
import matplotlib.pyplot as plt


def random_utilities(participants: [int], number_of_gifts: int, max_utility=None) -> {str: [int]}:
    if max_utility is None:
        max_utility = number_of_gifts + np.floor(number_of_gifts/2)
    utilities = {}
    for p in participants:
        utility = [rand.randint(1, max_utility) for _ in range(number_of_gifts)]
        utilities.update({p: utility})

    return utilities


def normalized_utilities(participants: [int], number_of_gifts: int) -> {str: [int]}:
    utilities = {}
    for p in participants:
        base_utility = [i for i in range(number_of_gifts)]
        utility = []
        for _ in range(number_of_gifts):
            u = base_utility.pop(rand.randint(0, len(base_utility))-1)
            utility.append(u)
        utilities.update({p: utility})

    return utilities


def generate_sites(n, m, max_weight):
    g = nx.gnm_random_graph(n, m)
    for e in list(g.edges()):
        x = e[0]
        y = e[1]
        g[x][y]['weight'] = rand.randint(1, max_weight)

    return g


def initializer(number_of_agents=3, vertices_number=13, max_weight=10):
    edges_number = (vertices_number * (vertices_number - 1)) / 2
    agents = [i for i in range(number_of_agents)]

    sites = generate_sites(vertices_number, edges_number, max_weight)
    while not nx.is_connected(sites):
        sites = generate_sites(vertices_number, edges_number, max_weight)

    positions, free_sites = place_agents(agents, sites)

    return agents, sites, positions, free_sites, max_weight


def draw_graph(g: nx.Graph):
    nx.draw(g)
    plt.show()


def aff_graph(graph: nx.Graph):
    nodes = list(graph.nodes())
    edges = graph.edges()
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
        print('graph[' + str(x) + '][' + str(y) + '][weight]: ' + str(graph[x][y]['weight']))


def place_agents(agents: [int], sites: nx.Graph):
    # init agents location
    positions = {}
    free_sites = list(sites.nodes())

    for a in agents:
        s_len = len(free_sites)
        idx = rand.randint(0, s_len - 1)
        node = free_sites.pop(idx)
        positions.update({a: [node]})

    return positions, free_sites
