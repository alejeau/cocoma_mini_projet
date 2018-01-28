#!/usr/bin/python3
# -*-coding: utf-8 -*

from tools import tools
from protocols import yankee_swap
from protocols.tools import yankee_tools


def main_yankee_swap():
    # letters = 'abcdefghijklmnopqrstuvwxyz'
    number_of_participants = 6
    number_of_gifts = 13
    # participants = [letters[i] for i in range(number_of_participants)]
    participants = [i for i in range(number_of_participants)]
    gifts = [i for i in range(number_of_gifts)]
    # utilities = tools.random_utilities(participants, number_of_gifts)
    utilities = tools.normalized_utilities(participants, number_of_gifts)

    print('participants: ' + str(participants))
    print('gifts: ' + str(gifts))
    print('utilities' + str(utilities))

    allocations = yankee_swap.yankee_swap(participants, gifts, utilities)
    print('allocations: ' + str(allocations))

    touring_costs = yankee_tools.tour_cost(allocations)
    print('\ntouring_costs: ')
    for agent in sorted(touring_costs.keys()):
        print('\t' + str(agent) + ': ' + str(touring_costs[agent]))

    esw = yankee_tools.egalitarian_social_welfare(allocations, utilities)
    print('\nEgalitarian social welfare: ')
    for agent in sorted(esw.keys()):
        score = yankee_tools.allocation_utility(allocations[agent], utilities[agent])
        print('\t' + str(agent) + ', score: ' + str(score))
        print('\t' + str(agent) + ': ' + str(esw[agent]))

    pfs = yankee_tools.proportional_fair_share(allocations, utilities)
    print('\nProportional fair share: ')
    for agent in sorted(pfs.keys()):
        share = pfs[agent]
        fairness = 'fair' if share[2] else 'unfair'
        utility = yankee_tools.allocation_utility(allocations[agent], utilities[agent])
        print('\tThe allocation for agent \'' + str(agent) + '\' with value ' + str(utility) + ' is ' + fairness + ' ' + str(share))

    envy = yankee_tools.envy_freeness(allocations, utilities)
    if envy:
        print('\nEnvy freeness: ')
        for agent in sorted(envy.keys()):
            score = yankee_tools.allocation_utility(allocations[agent], utilities[agent])
            print('\t' + str(agent) + ', score: ' + str(score))
            print('\t' + str(agent) + ': ' + str(envy[agent]))
    else:
        print('\nThe allocation is envy-free')


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
        score = yankee_tools.allocation_utility(allocations[agent], utilities[agent])
        print('\t' + str(agent) + ', score: ' + str(score))
        print('\t' + str(agent) + ': ' + str(esw[agent]))

    envy = yankee_tools.envy_freeness(allocations, utilities)
    if envy:
        print('Envy freeness: ')
        for agent in sorted(envy.keys()):
            score = yankee_tools.allocation_utility(allocations[agent], utilities[agent])
            print('\t' + str(agent) + ', score: ' + str(score))
            print('\t' + str(agent) + ': ' + str(envy[agent]))
    else:
        print('The allocation is envy-free')


main_yankee_swap()
# main_tools_testing()
