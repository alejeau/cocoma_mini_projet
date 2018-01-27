#!/usr/bin/python3
# -*-coding: utf-8 -*

import networkx as nx
from tools import tools
from protocols import sequential, sequential_regrets
from protocols.tools import sequential_tools


def initializer():
    number_of_agents = 3
    vertices_number = 13
    edges_number = (vertices_number * (vertices_number - 1)) / 2
    max_weight = 10
    agents = [i for i in range(number_of_agents)]

    sites = tools.generate_sites(vertices_number, edges_number, max_weight)
    while not nx.is_connected(sites):
        sites = tools.generate_sites(vertices_number, edges_number, max_weight)

    positions, free_sites = tools.place_agents(agents, sites)

    return agents, sites, positions, free_sites, max_weight


def initializer_solo():
    number_of_agents = 1
    vertices_number = 7
    edges_number = (vertices_number * (vertices_number - 1)) / 2
    max_weight = 10
    agents = [i for i in range(number_of_agents)]

    sites = tools.generate_sites(vertices_number, edges_number, max_weight)
    while not nx.is_connected(sites):
        sites = tools.generate_sites(vertices_number, edges_number, max_weight)

    positions, free_sites = tools.place_agents(agents, sites)

    return agents, sites, positions, free_sites, max_weight


def main_sequential(agents, sites, positions, free_sites, max_weight):
    allocations, tour_costs = sequential.sequential_auctions(agents, sites, positions, free_sites, max_weight)
    print('allocations: ' + str(allocations))
    print('tour_costs: ' + str(tour_costs))

    sites_utility = sequential_tools.sites_utility(sites)
    print('sites_utility: ' + str(sites_utility))

    pfs = sequential_tools.proportional_fair_share(allocations, tour_costs, sites)
    print('\nProportional fair share: ')
    for agent in sorted(pfs.keys()):
        share = pfs[agent]
        fairness = 'fair' if share[2] else 'unfair'
        utility = sum(tour_costs[agent])
        print('\tThe allocation for agent \'' + str(agent) + '\' with value ' + str(utility) + ' is ' + fairness + ' ' + str(share))


def main_sequential_regrets(agents, sites, positions, free_sites, max_weight):
    allocations, tour_costs = sequential_regrets.sequential_auctions_with_regret(agents, sites, positions, free_sites, max_weight)
    print('allocations: ' + str(allocations))
    print('tour_costs: ' + str(tour_costs))

    sites_utility = sequential_tools.sites_utility(sites)
    print('sites_utility: ' + str(sites_utility))


def main():
    agents, sites, positions, free_sites, max_weight = initializer()

    main_sequential(agents, sites, positions, free_sites, max_weight)
    # main_sequential_regrets(agents, sites, positions, free_sites, max_weight)


def main_test():
    agents, sites, positions, free_sites, max_weight = initializer_solo()

    allocations, tour_costs = sequential.sequential_auctions(agents, sites, positions, free_sites, max_weight)
    print('allocations: ' + str(allocations))
    print('tour_costs: ' + str(tour_costs))

    sites_utility = sequential_tools.sites_utility(sites)
    print('sites_utility: ' + str(sites_utility))


main()
# main_test()
