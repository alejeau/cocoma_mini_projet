#!/usr/bin/python3
# -*-coding: utf-8 -*


def allocation_utility(allocation: [int], utility: [int]) -> int:
    score = 0
    for a in allocation:
        score += utility[a]

    return score


def tour_cost(tour: {str: [int]}) -> {str: int}:
    costs = {}
    for agent in tour.keys():
        cost = len(tour[agent])
        costs.update({agent: cost})

    return costs


def egalitarian_social_welfare(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: [([int], int)]}:
    utility_scores = {}
    for agent in allocations.keys():
        score = allocation_utility(allocations[agent], utilities[agent])
        utility_scores.update({agent: score})

    print('utility_scores: ' + str(utility_scores))

    worst_score = max(utility_scores.values())
    print('worst_score: ' + str(worst_score))
    worst_off_agents = []
    for agent in utility_scores.keys():
        if utility_scores[agent] == worst_score:
            worst_off_agents.append(agent)

    wronged_agents = {}
    for woa in worst_off_agents:
        better_allocations = []
        utility = utilities[woa]
        for agent in allocations.keys():
            allocation = allocations[agent]
            score = allocation_utility(allocation, utility)
            if score < worst_score:
                better_allocations.append((agent, allocation, score))
        if len(better_allocations) > 0:
            wronged_agents.update({woa: better_allocations})

    return wronged_agents


def proportional_fair_share(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: [([int], int)]}:
    pfs = {}
    agents = allocations.keys()
    number_of_agents = len(agents)
    for agent in agents:
        share = sum(utilities[agent]) / number_of_agents
        utility = utilities[agent]
        allocation = allocations[agent]
        prop = True if allocation_utility(allocation, utility) <= share else False
        pfs.update({agent: (share, allocation, prop)})

    return pfs


def envy_freeness(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: [([int], int)]}:
    utility_scores = {}
    for agent in allocations.keys():
        score = allocation_utility(allocations[agent], utilities[agent])
        utility_scores.update({agent: score})

    envious_agents = {}
    for agent in allocations.keys():
        better_allocations = []
        utility = utilities[agent]
        agent_score = utility_scores[agent]
        for other in allocations.keys():
            if agent != other:
                allocation = allocations[other]
                score = allocation_utility(allocation, utility)
                if score < agent_score:
                    better_allocations.append((other, allocation, score))
            if len(better_allocations) > 0:
                envious_agents.update({agent: better_allocations})

    return envious_agents
