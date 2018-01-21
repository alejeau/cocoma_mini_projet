#!/usr/bin/python3
# -*-coding: utf-8 -*

import networkx as nx
from tools import tools
from auctions import sequential
from Archivist import Archivist


max_weight = 10
log = Archivist()
log.open_file('log.txt')


def main_sequential():
    vertex = 7
    g = tools.generate_sites(vertex, 2*vertex-2, max_weight)

    while not nx.is_connected(g):
        g = tools.generate_sites(vertex, 2*vertex-2, max_weight)

    agents = [0, 1]
    results = sequential.sequential_auctions(agents, g, max_weight)
    print('results: ' + str(results))


main_sequential()

log.close()
