#!/usr/bin/python3
# -*-coding: utf-8 -*

import random as rand
import networkx as nx
from tools import tools
from protocols import sequential, sequential_regrets, yankee_swap
from Archivist import Archivist


log = Archivist()
log.open_file('log.txt')


def initializer():
    number_of_agents = 2
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
    results = sequential.sequential_auctions(agents, sites, positions, free_sites, max_weight)
    print('results: ' + str(results))


def main_sequential_regrets(agents, sites, positions, free_sites, max_weight):
    results = sequential_regrets.sequential_auctions_with_regret(agents, sites, positions, free_sites, max_weight)
    print('results: ' + str(results))


def main_yankee_swap():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    number_of_participants = 6
    participants = [letters[i] for i in range(number_of_participants)]
    gifts = [i for i in range(number_of_participants)]
    utilities = {}
    for p in participants:
        utility = [rand.randint(1, 10) for _ in range(number_of_participants)]
        utilities.update({p: utility})

    print('participants: ' + str(participants))
    print('gifts: ' + str(gifts))
    print('utilities' + str(utilities))

    results = yankee_swap.yankee_swap(participants, gifts, utilities)
    print('results: ' + str(results))


def main():
    agents, sites, positions, free_sites, max_weight = initializer()

    main_sequential(agents, sites, positions, free_sites, max_weight)
    main_sequential_regrets(agents, sites, positions, free_sites, max_weight)


# main()
main_yankee_swap()
log.close()
