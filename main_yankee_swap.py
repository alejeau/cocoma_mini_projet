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
    utility_max = number_of_gifts + np.floor(number_of_gifts/2)
    utilities = {}
    for p in participants:
        utility = [rand.randint(1, utility_max) for _ in range(number_of_gifts)]
        utilities.update({p: utility})

    # print('participants: ' + str(participants))
    # print('gifts: ' + str(gifts))
    # print('utilities' + str(utilities))

    results = yankee_swap.yankee_swap(participants, gifts, utilities)
    print('results: ' + str(results))

    touring_costs = yankee_tools.tour_cost(results)
    print('touring_costs: ')
    for agent in sorted(touring_costs.keys()):
        print('\t' + str(agent) + ': ' + str(touring_costs[agent]))


main_yankee_swap()
log.close()
