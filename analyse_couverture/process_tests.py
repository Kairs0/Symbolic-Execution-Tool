#!/usr/bin/env python
# -*- coding: utf-8 -*-

# while loop is made with a second node which points to the while node


def process_value_test(x, graph, y=0):
    path = []
    next_node = 1
    path.append(next_node)
    limit = 0
    while next_node != 0 and limit <= 100:
        node = graph[next_node]
        # print(node)
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
            consigne_x = node[1]
            consigne_y = node[2]
            # print("consigne: x=" + consigne.replace("x", str(x)))
            if consigne_x != "":
                x = eval(consigne_x.replace("x", str(x)))

            if consigne_y != "":
                y = eval(consigne_y.replace("y", str(y)))

            next_node = node[3]

        path.append(next_node)
        limit += 1
    return path
    # print("final value: " + str(x))
    # print("final step: " + str(next_node))
    # print("path:" + str(path))


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


def toutes_affectation(valeurs_test, graph):
    print("Critère: toutes les affectations")

    objective = []
    for key, value in graph.items():
        if value[0] == "assign":
            objective.append(key)

    print("We want the following nodes to be visited: " + str(objective))

    # print("test values processed:" + str(valeurs_test))
    for value in valeurs_test:
        path = process_value_test(value, graph)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        print("TA is operational")
    else:
        print("TA fails:")
        print("Nodes " + str(objective) + " were never reached.")


def toutes_decisions(valeurs_test, graph):
    print("Critère: toutes les décisions")

    objective = []
    for key, value in graph.items():
        if value[0] == "if" or value[0] == "while":
            objective.append(key)
            for following_nodes in value[3]:
                objective.append(following_nodes)

    for value in valeurs_test:
        path = process_value_test(value, graph)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        print("TD is operational")
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

    toutes_affectation(test_values, new_graph_prog)
    toutes_decisions(test_values, new_graph_prog)

    toutes_affectation(test_values, new_test_two_variables)
    toutes_decisions(test_values, new_test_two_variables)
