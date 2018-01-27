#!/usr/bin/python3
# -*-coding: utf-8 -*


def tour_cost(tour: {str: [int]}) -> {str: int}:
    costs = {}
    for agent in tour.keys():
        cost = len(tour[agent])
        costs.update({agent: cost})

    return costs


def egalitarian_social_welfare(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: int}:
    pass
