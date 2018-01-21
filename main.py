#!/usr/bin/python3
# -*-coding: utf-8 -*

import networkx as nx
from tools import tools
from auctions import sequential, sequential_regrets
from Archivist import Archivist


log = Archivist()
log.open_file('log.txt')


def initializer():
    vertex = 7
    max_weight = 10
    sites = tools.generate_sites(vertex, 2 * vertex - 2, max_weight)

    while not nx.is_connected(sites):
        sites = tools.generate_sites(vertex, 2 * vertex - 2, max_weight)

    agents = [0, 1]
    positions, free_sites = tools.place_agents(agents, sites)

    return agents, sites, positions, free_sites, max_weight


def main_sequential(agents, sites, positions, free_sites, max_weight):
    results = sequential.sequential_auctions(agents, sites, positions, free_sites, max_weight)
    print('results: ' + str(results))


def main_sequential_regrets(agents, sites, positions, free_sites, max_weight):
    results = sequential_regrets.sequential_auctions_with_regret(agents, sites, positions, free_sites, max_weight)
    print('results: ' + str(results))


def main():
    agents, sites, positions, free_sites, max_weight = initializer()

    main_sequential(agents, sites, positions, free_sites, max_weight)
    main_sequential_regrets(agents, sites, positions, free_sites, max_weight)


main()
log.close()
