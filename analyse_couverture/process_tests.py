#!/usr/bin/env python
# -*- coding: utf-8 -*-

# while loop is made with a second node which points to the while node


def process_value_test(x, graph, variables, y=0):
    # TODO: replace these two affectation in order to:
    #  - either match the variables in the graph
    #  - or make the affectation before, while parsing the text file (requires matching
    # test file and variables from the program tested)
    variables['x'] = x
    variables['y'] = y
    path = []
    next_node = 1
    path.append(next_node)
    count = 0
    limit = 100  # TODO: limit has been put to 100 avoid infinite loop. To remove or increment value
    while next_node != 0 and count <= limit:
        node = graph[next_node]
        if node[0] == "if" or node[0] == "while":
            # TODO: check if ok for while
            values = node[2]
            next_node = comparison(eval(str(values[0])),
                                   eval(str(values[1])),
                                   node[1],
                                   node[3][0],
                                   node[3][1]
                                   )
        elif node[0] == "skip":
            next_node = node[1]
        elif node[0] == "assign":
            instruct = node[1]
            # instruct: {'x': 'x+1'}
            for key, instruction in instruct.items():
                variables[key] = eval(instruction.replace(key, str(variables[key])))
            next_node = node[2]

        path.append(next_node)
        count += 1
    return path


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
        # dic to dynamically keep track of variables
        variables = {}
        path = process_value_test(value, graph, variables)
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
        # dic to dynamically keep track of variables
        variables = {}
        path = process_value_test(value, graph, variables)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        print("TD: OK")
    else:
        print("TD fails:")
        print("Nodes " + str(objective) + " were never reached.")


if __name__ == '__main__':

    PATH_TESTS = "tests_txt/test.txt"

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

    test_values = []
    with open(PATH_TESTS) as file:
        for line in file:
            test_values.append(int(line))

    all_affectations(test_values, graph_prog)
    all_decisions(test_values, graph_prog)
    all_affectations(test_values, test_two_variables)
    all_decisions(test_values, test_two_variables)
