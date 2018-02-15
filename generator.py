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
            target.reverse()
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


def generate_sets_tests(graph_prog, path_folder_to_write, name_file='generated.txt'):
    all_results = {}
    result_all_aff = all_affectations(graph_prog)

    for key, value in result_all_aff.items():
        if key not in all_results:
            all_results[key] = value
        else:
            all_results[key] += value

    result_all_dec = all_decisions(graph_prog)

    for key, value in result_all_dec.items():
        if key not in all_results:
            all_results[key] = value
        else:
            all_results[key] += value

    result_k_paths = all_k_paths(graph_prog, 10)

    for key, value in result_k_paths.items():
        if key not in all_results:
            all_results[key] = value
        else:
            all_results[key] += value

    # TODO: concat others generated files

    # remove duplicates in all value of all_results:
    for key, value in all_results.items():
        all_results[key] = list(set(value))

    len_longest = 0
    for values in all_results.values():
        if len(values) > len_longest:
            len_longest = len(values)

    # write values on disk
    with open(path_folder_to_write + '/' + name_file, 'w') as file:
        for i in range(len_longest):
            array_to_write = []
            for key, value in all_results.items():
                try:
                    array_to_write.append(key + ':' + str(value[i]))
                except IndexError:
                    array_to_write.append(key + ':' + str(0))

            str_to_write = ",".join(array_to_write) + "\n"
            file.write(str_to_write)
        file.close()


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
    # print(result_all_aff)

    result_all_dec = all_decisions(graph)
    # print(result_all_dec)

    result_k_paths = all_k_paths(graph, 10)
    # print(result_k_paths)


if __name__ == "__main__":
    main()
