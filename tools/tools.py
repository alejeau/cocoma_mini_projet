#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
import networkx as nx
import matplotlib.pyplot as plt


def generate_sites(n, m, max_weight):
    g = nx.gnm_random_graph(n, m)
    for e in list(g.edges()):
        x = e[0]
        y = e[1]
        g[x][y]['weight'] = random.randint(1, max_weight)

    return g


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
        idx = random.randint(0, s_len - 1)
        node = free_sites.pop(idx)
        positions.update({a: [node]})

    return positions, free_sites
