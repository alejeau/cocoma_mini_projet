#!/usr/bin/python3
# -*-coding: utf-8 -*


# def tour_cost(tour: {str: [int]}) -> {str: int}:
def tour_cost(tour):
    costs = {}
    for agent in tour.keys():
        cost = len(tour[agent])
        costs.update({agent: cost})

    return costs


# def egalitarian_social_welfare(allocations: {str: [int]}, utilities: {str: [int]}) -> {str: int}:
def egalitarian_social_welfare(allocations, utilities):
    pass
