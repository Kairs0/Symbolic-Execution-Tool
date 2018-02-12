#!/usr/bin/env python
# -*- coding: utf-8 -*-

from symbolic_exec_tools import generate_value, get_all_var


def all_affectations(graph):
    objectives = []
    for key, value in graph.items():
        if value[0] == "assign":
            objectives.append(key)

    variables = get_all_var(graph)
    solutions = []

    for objective in objectives:
        solutions.append(generate_value(graph, objective))

    merge_solutions = {}
    # merge solution dictionaries
    # how to deal with multiple solutions ?
    # TODO: en cours
    for solution in solutions:
        for key, value in solution:
            if key in merge_solutions:
                merge_solutions[key].append()

