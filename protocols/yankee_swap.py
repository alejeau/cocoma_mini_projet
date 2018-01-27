#!/usr/bin/python3
# -*-coding: utf-8 -*

import copy


# def yankee_swap(participants: [str], gifts: [int], utilities: {str: [int]}) -> {str: int}:
def yankee_swap(participants, gifts, utilities):
    """
    Implements the yankee swap protocol for n agents and m wrapped gifts.
    The gifts are chosen based on the maximum utility.

    Each gift can only be stolen once per turn, and three times total.
    None of the function's parameters will be modified.

    Parameters
    ----------
    participants: [str]
        the ordered tuple of participating agents: (b, c, a) means b goes first, c second and a third
    gifts: [int]
        the list of wrapped gifts. As long as a gift as not been opened, it's value is unknown
    utilities: {str: [int]}
        for each agent, an ordered list of the utility for each gift, as in {'agent_a': [10, 7, 3, 4]} means that the
        agent_a's utility of gift 0 is utilities['agent_a'][0], which here is 10.

    Returns
    -------
    {str: [int]}
        a dict with the agent as key and a list of the collected gifts
    """
    agents = tuple(participants)
    wrapped_gifts = copy.deepcopy(gifts)
    unwrapped_gifts = []
    locked_gifts = []
    frozen_gifts = {}
    allocations = {}

    for agent in agents:
        allocations.update({agent: []})
        
    while wrapped_gifts:
        for i in range(len(agents)):
            agent = agents[i]
            best_gift = -1
            agent_utilities = utilities[agent]
            avg_utility = sum(agent_utilities) / len(agent_utilities)
            for gift in unwrapped_gifts:
                if frozen_gifts.get(gift, 0) < 3 and gift not in locked_gifts and agent_utilities[gift] < avg_utility:
                    if best_gift == -1:
                        best_gift = gift
                    elif agent_utilities[gift] > agent_utilities[best_gift]:
                        best_gift = gift
                        
            # if we chose to steal a gift
            if best_gift != -1:
                locked_gifts.append(best_gift)
                tmp = frozen_gifts.get(best_gift, 0)
                frozen_gifts.update({best_gift: tmp+1})
                for tmp in agents:
                    if best_gift in allocations[tmp]:
                        gift_list = allocations[tmp]
                        gift_list.remove(best_gift)
                        allocations.update({tmp: gift_list})
            else:
                if len(wrapped_gifts) != 0:
                    best_gift = wrapped_gifts.pop(0)
                    unwrapped_gifts.append(best_gift)

            # if we choose not to steal a gift and the list of unwrapped gifts is empty, we get no gift
            if best_gift != -1:
                gift_list = allocations.get(agent, [])
                gift_list.append(best_gift)
                allocations.update({agent: gift_list})
        locked_gifts = []
    return allocations
