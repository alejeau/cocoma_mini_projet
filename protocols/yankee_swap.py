#!/usr/bin/python3
# -*-coding: utf-8 -*

import copy


def yankee_swap(participants: [str], gifts: [int], utilities: {str: [int]}) -> {str: int}:
    """
    Implements the yankee swap protocol for x agents and x wrapped gifts.

    Each gift can only be stolen once per turn. None of the function's parameters will be modified.

    Parameters
    ----------
    agents: [str]
        the ordered tuple of participating agents: (b, c, a) means b goes first, c second and a third
    gifts: [int]
        the list of wrapped gifts. As long as a gift as not been opened, it's value is unknown
    utilities: {str: [int]}
        for each agent, an ordered list of the utility for each gift, as in {'agent_a': [10, 7, 3, 4]} means that the
        agent_a's utility of gitf 0 is utilities['agent_a'][0], which here is 10.

    Returns
    -------
    {str: int}
        a dict with the agent as key and the gift as value
    """
    agents = tuple(participants)
    wrapped_gifts = copy.deepcopy(gifts)
    unwrapped_gifts = []
    allocations = {}

    for agent in agents:
        allocations.update({agent: -1})

    return allocations
