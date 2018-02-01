#!/usr/bin/env python
# -*- coding: utf-8 -*-

LIMIT_FOR_INFINITE_LOOP = 100


def process_value_test(graph, variables):
    path = []
    next_node = 1
    path.append(next_node)
    count = 0
    while next_node != 0 and count <= LIMIT_FOR_INFINITE_LOOP:
        node = graph[next_node]
        if node[0] == "if" or node[0] == "while":
            # TODO: check if ok for while
            values = node[2]
            # adapt to dic
            next_node = comparison(
                variables[values[0]] if values[0] in variables else values[0],
                variables[values[1]] if values[1] in variables else values[1],
                node[1],
                node[3][0],
                node[3][1]
            )

        elif node[0] == "skip":
            next_node = node[1][0]
        elif node[0] == "assign":
            instruct = node[1]
            for key, instruction in instruct.items():
                variables[key] = eval(replace_any_var_by_value(instruction, variables))
            next_node = node[2][0]

        path.append(next_node)
        count += 1
    return path, variables


def replace_any_var_by_value(instruction, variables):
    for key, value in variables.items():
        instruction = instruction.replace(key, str(variables[key]))
    return instruction


def comparison(a, b, operator, out1, out2):
    if operator == "<=":
        if a <= b:
            return out1
        else:
            return out2
    elif operator == "<":
        if a < b:
            return out1
        else:
            return out2
    elif operator == "==":
        if a == b:
            return out1
        else:
            return out2
    elif operator == ">":
        if a > b:
            return out1
        else:
            return out2
    elif operator == ">=":
        if a >= b:
            return out1
        else:
            return out2


def all_affectations(values_test, graph):
    print("Criterion: all affectations")

    objective = []
    for key, value in graph.items():
        if value[0] == "assign":
            objective.append(key)

    print("We want the following nodes to be visited: " + str(objective))

    for value in values_test:
        path, var = process_value_test(graph, value)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        print("TA: OK")
    else:
        print("TA fails:")
        print("Nodes " + str(objective) + " were never reached.")


def all_decisions(values_test, graph):
    print("Criterion: all decisions")

    objective = []
    for key, value in graph.items():
        if value[0] == "if" or value[0] == "while":
            objective.append(key)
            for following_nodes in value[3]:
                objective.append(following_nodes)

    print("We want the following nodes to be visited: " + str(objective))

    for value in values_test:
        path, var = process_value_test(graph, value)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        print("TD: OK")
    else:
        print("TD fails:")
        print("Nodes " + str(objective) + " were never reached.")


def get_all_paths(graph, start, end, path=None):
    if path is None:
        path = []

    if start == 0:
        # end of graph
        return [path]

    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for node in graph[start][-1]:
        if node not in path:
            new_paths = get_all_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


# def all_k_paths(values_test, graph, k):
#     print("Criterion: all k paths for k = " + str(k))
#     objective = []
#     for key, value in graph.items():
#         pass  # TODO
#
#     print("We want the following nodes to be visited: " + str(objective))
#
#     for value in values_test:
#         path, var = process_value_test(graph, value)
#         for step in path:
#             if step in objective:
#                 objective.remove(step)
#
#     if len(objective) == 0:
#         print("All k paths: OK")
#     else:
#         print("All k paths fails:")
#         print("Nodes " + str(objective) + " were never reached.")


def read_test_file(path_tests):
    values_tests = []
    with open(path_tests) as file:
        for line in file:
            variables = {}
            assignments = line.split(",")
            for assignment in assignments:
                var = assignment.split(":")[0]
                value = assignment.split(":")[1]
                variables[var] = int(value)
            values_tests.append(variables)
    return values_tests


if __name__ == '__main__':

    PATH_TESTS = "sets_tests_txt/test.txt"

    # Hand written CFG graphs
    # (temporary - while ast_to_cfg isn't connected to process_tests)

    test_two_variables = {
        1: ['if', '<=', ['x', 0], [2, 3]],
        2: ['assign', {'y': 'x'}, 4],
        3: ['assign', {'y': '0-x'}, 4],
        4: ['assign', {'x': 'y*2'}, 0]
    }

    graph_prog = {
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '0-x'}, 4],
            3: ['assign', {'x': '1-x'}, 4],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, 0],
            6: ['assign', {'x': 'x+1'}, 0]
        }

    test_values = read_test_file(PATH_TESTS)
    all_affectations(test_values, test_two_variables)
    test_values = read_test_file(PATH_TESTS)
    all_decisions(test_values, test_two_variables)
    test_values = read_test_file(PATH_TESTS)
    all_affectations(test_values, graph_prog)
    test_values = read_test_file(PATH_TESTS)
    all_decisions(test_values, graph_prog)
