#!/usr/bin/env python
# -*- coding: utf-8 -*-

from symbolic_exec_tools import generate_value_from_node, generate_value_from_path
from process_cfg_tools import get_all_k_paths_brute


def all_affectations(graph):
    objectives = []
    for key, value in graph.items():
        if value[0] == "assign":
            objectives.append(key)

    solutions = []

    for objective in objectives:
        # /!\ generate_value_from_node seems to be a dic, but it could be a list of dic!
        result_objective = generate_value_from_node(graph, objective)
        if isinstance(result_objective, dict):
            solutions.append(result_objective)
        elif isinstance(result_objective, list):
            solutions.extend(result_objective)

    merge_solutions = {}
    # merge solution dictionaries
    # multiple solutions -> we always get the first that contain our solution (?)
    for solution in solutions:
        for key, value in solution.items():
            if key in merge_solutions:
                merge_solutions[key].append(value)
            else:
                merge_solutions[key] = [value]

    # remove double in list
    for key, value in merge_solutions.items():
        merge_solutions[key] = list(set(value))

    return merge_solutions


def all_decisions(graph):
    objectives = []
    for key, value in graph.items():
        if value[0] == "if" or value[0] == "while":
            objectives.append(key)
            for following_nodes in value[-1]:
                objectives.append(following_nodes)

    solutions = []

    for objective in objectives:
        # /!\ generate_value_from_node seems to be a dic, but it could be a list of dic!
        result_objective = generate_value_from_node(graph, objective)
        if isinstance(result_objective, dict):
            solutions.append(result_objective)
        elif isinstance(result_objective, list):
            solutions.extend(result_objective)

    merge_solutions = {}
    # merge solution dictionaries
    # multiple solutions -> we always get the first that contain our solution (?)
    for solution in solutions:
        for key, value in solution.items():
            if key in merge_solutions:
                merge_solutions[key].append(value)
            else:
                merge_solutions[key] = [value]

    # remove double in list
    for key, value in merge_solutions.items():
        merge_solutions[key] = list(set(value))

    return merge_solutions


def all_k_paths(graph, k):
    target_paths = get_all_k_paths_brute(graph, k)

    # remove 0 for all targets
    for target in target_paths:
        target.remove(0)

    solutions = []

    for target in target_paths:
        # /!\ generate_value_from_node seems to be a dic, but it could be a list of dic!
        result_objective = generate_value_from_path(graph, target)
        if isinstance(result_objective, dict):
            solutions.append(result_objective)
        elif isinstance(result_objective, list):
            solutions.extend(result_objective)
        elif result_objective is None:
            print("[All k-paths] Impossible to cover path " + str(target))

    merge_solutions = {}
    # merge solution dictionaries
    # multiple solutions -> we always get the first that contain our solution (?)
    for solution in solutions:
        for key, value in solution.items():
            if key in merge_solutions:
                merge_solutions[key].append(value)
            else:
                merge_solutions[key] = [value]

    # remove double in list
    for key, value in merge_solutions.items():
        merge_solutions[key] = list(set(value))

    return merge_solutions


def main():
    graph = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0 - x'}, [4]],
            3: ['assign', {'x': '1 - x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x + 1'}, [0]]
    }

    # result {'x': [0, 49, -1], 'y':[43, 6]}
    result_all_aff = all_affectations(graph)
    print(result_all_aff)

    result_all_dec = all_decisions(graph)
    print(result_all_dec)

    result_k_paths = all_k_paths(graph, 10)
    print(result_k_paths)


if __name__ == "__main__":
    main()
