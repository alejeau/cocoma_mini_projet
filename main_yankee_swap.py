#!/usr/bin/python3
# -*-coding: utf-8 -*

import numpy as np
import random as rand
from protocols.tools import yankee_tools
from protocols import yankee_swap
from Archivist import Archivist


log = Archivist()
log.open_file('log.txt')


def main_yankee_swap():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    number_of_participants = 6
    number_of_gifts = 12
    participants = [letters[i] for i in range(number_of_participants)]
    gifts = [i for i in range(number_of_gifts)]
    utilities = {}
    for p in participants:
        base_utility = [i for i in range(number_of_gifts)]
        utility = []
        for _ in range(number_of_gifts):
            u = base_utility.pop(rand.randint(0, len(base_utility))-1)
            utility.append(u)
        utilities.update({p: utility})

    print('participants: ' + str(participants))
    print('gifts: ' + str(gifts))
    print('utilities' + str(utilities))

    allocations = yankee_swap.yankee_swap(participants, gifts, utilities)
    print('allocations: ' + str(allocations))

    touring_costs = yankee_tools.tour_cost(allocations)
    print('touring_costs: ')
    for agent in sorted(touring_costs.keys()):
        print('\t' + str(agent) + ': ' + str(touring_costs[agent]))

    esw = yankee_tools.egalitarian_social_welfare(allocations, utilities)
    print('Egalitarian social welfare: ')
    for agent in sorted(esw.keys()):
        score = yankee_tools.utility_score(allocations[agent], utilities[agent])
        print('\t' + str(agent) + ', score: ' + str(score))
        print('\t' + str(agent) + ': ' + str(esw[agent]))

    envy = yankee_tools.envy_freeness(allocations, utilities)
    if envy:
        print('Envy freeness: ')
        for agent in sorted(envy.keys()):
            score = yankee_tools.utility_score(allocations[agent], utilities[agent])
            print('\t' + str(agent) + ', score: ' + str(score))
            print('\t' + str(agent) + ': ' + str(envy[agent]))
    else:
        print('The allocation is envy-free')


def main_tools_testing():
    utilities = {
        'a': [0, 7, 5, 2, 3, 4, 10, 11, 9, 8, 1, 6],
        'b': [2, 5, 9, 8, 3, 11, 7, 1, 4, 0, 10, 6],
        'c': [0, 8, 6, 5, 11, 10, 7, 4, 9, 3, 1, 2],
        'd': [3, 11, 7, 4, 1, 10, 5, 0, 8, 9, 6, 2],
        'e': [6, 2, 11, 5, 10, 9, 1, 8, 4, 7, 0, 3],
        'f': [3, 1, 11, 10, 8, 5, 2, 4, 9, 0, 7, 6]
    }
    allocations = {
        'a': [2, 5, 4, 10],
        'b': [1, 8],
        'c': [3, 7],
        'd': [0, 6],
        'e': [11],
        'f': [9]
    }

    esw = yankee_tools.egalitarian_social_welfare(allocations, utilities)
    print('Egalitarian social welfare: ')
    for agent in sorted(esw.keys()):
        score = yankee_tools.utility_score(allocations[agent], utilities[agent])
        print('\t' + str(agent) + ', score: ' + str(score))
        print('\t' + str(agent) + ': ' + str(esw[agent]))

    envy = yankee_tools.envy_freeness(allocations, utilities)
    if envy:
        print('Envy freeness: ')
        for agent in sorted(envy.keys()):
            score = yankee_tools.utility_score(allocations[agent], utilities[agent])
            print('\t' + str(agent) + ', score: ' + str(score))
            print('\t' + str(agent) + ': ' + str(envy[agent]))
    else:
        print('The allocation is envy-free')


main_yankee_swap()
# main_tools_testing()
log.close()
