#!/usr/bin/env python
# -*- coding: utf-8 -*-

# while loop is made with a second node which points to the while node


def process_value_test(x, graph, y=0):
    path = []
    next_node = 1
    path.append(next_node)
    limit = 0  # TODO: limit has been put to avoid infinite loop. To remove or increment value
    while next_node != 0 and limit <= 100:
        node = graph[next_node]
        if node[0] == "if" or node[0] == "while":
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
            instruction_x = node[1]
            instruction_y = node[2]
            if instruction_x != "":
                x = eval(instruction_x.replace("x", str(x)))

            if instruction_y != "":
                y = eval(instruction_y.replace("y", str(y)))

            next_node = node[3]

        path.append(next_node)
        limit += 1
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
        path = process_value_test(value, graph)
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
        path = process_value_test(value, graph)
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

    new_graph_prog = {
        1: ["if", "<=", ["x", 0], [2, 3]],
        2: ["assign", "-x", "", 4],
        3: ["assign", "1-x", "", 4],
        4: ["if", "==", ["x", 1], [5, 6]],
        5: ["assign", "1", "", 0],
        6: ["assign", "x+1", "", 0]
    }

    new_test_two_variables = {
        1: ['if', '<=', ['x', 0], [2, 3]],
        2: ['assign', '', 'x', 4],
        3: ['assign', '', '0-x', 4],
        4: ['assign', 'y*2', '', 0]
    }

    test_values = []
    with open(PATH_TESTS) as file:
        for line in file:
            test_values.append(int(line))

    all_affectations(test_values, new_graph_prog)
    all_decisions(test_values, new_graph_prog)

    all_affectations(test_values, new_test_two_variables)
    all_decisions(test_values, new_test_two_variables)
