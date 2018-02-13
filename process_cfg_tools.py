#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides tools and functions in order to process a set of values on a program.
We expect a CFG graph for program processed and a dictionary of value for every variable of the program
"""

import random

LIMIT_FOR_INFINITE_LOOP = 100


def process_value_test(graph, variables, info_conditions=False):
    """
    :param graph: CFG graph
    :param variables: a dictionary {var: initial_value}
    :param info_conditions: a boolean, if true: will return an additional value which is a dic,
    stating how each condition was evaluated.
    :return: steps the program went through, dic of final values of variables, and perhaps a dic of
    value of boolean for each condition in a node.
    """
    path = []
    next_node = 1
    path.append(next_node)
    count = 0

    dic_result_cond = {}

    while next_node != 0 and count <= LIMIT_FOR_INFINITE_LOOP:
        if count == LIMIT_FOR_INFINITE_LOOP:
            raise ValueError('Infinite loop - program stopped')

        node = graph[next_node]
        if type_node(node) == "if" or type_node(node) == "while":
            bool_result = process_bool_expression(node[1], variables)  # check condition, returns True or False

            if info_conditions:
                dic_result_cond[next_node] = analyze_conditions(node[1], variables)

            next_node = node[-1][0] if bool_result else node[-1][1]
        elif type_node(node) == "skip":
            next_node = node[1][0]
        elif type_node(node) == "assign":
            instruct = node[1]
            for key, instruction in instruct.items():
                variables[key] = eval(replace_any_var_by_value(instruction, variables))
            next_node = node[2][0]

        path.append(next_node)
        count += 1

    if info_conditions:
        return path, variables, dic_result_cond
    else:
        return path, variables


def replace_any_var_by_value(instruction, variables):
    """
    Used to replace a variable by its current value
    :param instruction: a string 'a = b*3'
    :param variables: the dictionary of variables and their current values
    :return: the instruction to be executed
    """
    for key, value in variables.items():
        instruction = instruction.replace(key, str(value))
    return instruction


def type_node(node_value):
    """
    :param node_value: ['if', [[('<=', ["x", 0])]], [2, 3]]
    :return: Type of node ('if', 'assign', ...)
    """
    return node_value[0]


def is_boolean_expression_node(node_value):
    """
    Check whether a node in CFG contains a boolean expression or not
    :param node_value:
    :return:
    """
    if node_value[0] == 'while' or node_value[0] == 'if':
        return True
    else:
        return False


def process_bool_expression(conditions, variables):
    """
    :param conditions: [[(comp1), (comp2)],[(comp3), (comp4)]], each element is a list of conditions that
    must be respected (and logical gate)
    :param variables:
    :return: evaluated boolean expression
    """
    result = True
    # we want AND between each condition
    # -> if any of the condition is false, the result is false
    if any(not process_or_expression(condition, variables) for condition in conditions):
        result = False

    return result


def process_or_expression(conditions, variables):
    """
    :param conditions: [(comp1), (comp2)] List, each element being a condition, one of them must
    be respected (or logical gate)
    :param variables:
    :return: evaluated boolean expression
    """
    result = False
    # we want a OR between each condition
    # -> if only one condition is true, the result is true
    if any(process_condition(condition, variables) for condition in conditions):
        result = True

    return result


def process_condition(comparison, variables):
    """
    :param comparison:  ('<=', ["x", 0])
    :param variables: dictionary of variables in which we take the values
    :return: A boolean, stating if the condition is true or false
    """
    # comparison : tuple ('<=', ['x', 0])
    operator = comparison[0]
    values = comparison[1]

    # if variable in variable, pass its value, else pass the value
    # there will be an error if the variable given isn't inside the dictionary of variables
    return compare(
        operator,
        variables[values[0]] if values[0] in variables else values[0],
        variables[values[1]] if values[1] in variables else values[1],
    )


def analyze_conditions(bool_expr, variables):
    """
    For each condition in given boolean expression, returns the boolean evaluated.
    The result is returned as a list.
    :param bool_expr:
    :param variables: dic of variables and their values
    :return: list of booleans
    """

    conditions = get_conditions_from_bool_expression(bool_expr)
    result = []
    for comparison in conditions:
        operator = comparison[0]
        values = comparison[1]
        result_comparison = compare(
            operator,
            variables[values[0]] if values[0] in variables else values[0],
            variables[values[1]] if values[1] in variables else values[1],
        )
        result.append(result_comparison)

    return result


def compare(operator, a, b):
    """
    :param operator: a string which an operator ('==', '<=', ...)
    :param a: the first value to compare
    :param b: the second value to compare
    :return: boolean, result of the comparison
    """
    if operator == "<=":
        if a <= b:
            return True
        else:
            return False
    elif operator == "<":
        if a < b:
            return True
        else:
            return False
    elif operator == "==":
        if a == b:
            return True
        else:
            return False
    elif operator == ">":
        if a > b:
            return True
        else:
            return False
    elif operator == ">=":
        if a >= b:
            return True
        else:
            return False
    elif operator == "!=":
        if a != b:
            return True
        else:
            return False


def get_conditions_from_bool_expression(boolean_expression):
    """
    :param boolean_expression: simple: [[('<=', ['x', 0])]]
    and: [[('<=', ['x', 0])], [('>', ['y', 2])]]
    or: [[('<=', ['x', 0]), ('>', ['y', 2])]]
    complex: [[('<=', ['x', 0]), ('>', ['y', 2])], [('<=', ['x', 0]), ('>', ['y', 2])]]
    :return: list of conditions (syntax: ('<=', ['x', 0])), without any structure to distinguish between and/or
    """
    conditions = []
    for expressions in boolean_expression:
        for condition in expressions:
            conditions.append(condition)

    return conditions


def get_all_k_paths_brute(graph, k):
    """
    A brute force way to get k paths by choosing at each step randomly the next step.
    We iterate 100 times to be sure to cover all probables paths (TODO: justify why 100)
    :param graph:
    :param k:
    :return: a list of list, each list being a path [1, 4, 5]
    """
    paths = []

    limit = 100
    for i in range(limit):
        path = []
        next_step = 1
        for j in range(k):
            path.append(next_step)
            if next_step == 0:
                break
            next_step = random.choice(graph[next_step][-1])

        if path not in paths:
            paths.append(path)
    return paths


def get_all_paths(graph, start, path=None):
    """
    /!\ non functional when there are while loops
    Returns all path possible in a CFG graph given and from a starting point. Used for
    all k-path criteria test
    :param graph: a CFG graph
    :param start: a start point
    :param path: a list of step in current path, used for recursive call of the function
    :return: a list of list, each list being a path [1, 4, 5]
    """
    if path is None:
        path = []

    if start == 0:
        # end of graph
        return [path + [start]]

    path = path + [start]

    if start not in graph:
        return []

    paths = []
    for node in graph[start][-1]:
        if node not in path:

            new_paths = get_all_paths(graph, node, path)

            for new_path in new_paths:
                paths.append(new_path)
    return paths


def get_following_nodes(node_value):
    """
    For the value of a given node in a CFG graph, return the list of following(s) value(s)
    :param node_value: a value of a node in cfg
    :return: a list of steps
    """
    return node_value[-1]


def get_children(step_number, graph, visited=None):
    """
    For a graph and a given step number,
    Return the list of children (eg following nodes from this starting point)
    :param step_number: starting step_number
    :param graph: a CFG graph
    :param visited: argument used for recursive calls of function (a list of already visited nodes)
    :return: set: the list of following steps
    """
    if visited is None:
        visited = []

    children = []
    if step_number == 0:
        return children
    else:
        following_nodes = graph[step_number][-1]

        # we add the list of following nodes
        children.extend(following_nodes)

        # for each following node, we add their following nodes
        # to avoid issue when we encounter potential cycle, we keep track of visited nodes
        for following in [e for e in following_nodes if e not in visited]:
            visited.append(following)
            children.extend(get_children(following, graph, visited))

        return set(children)


def get_accessible_graph(graph, number_node):
    """
    Returns the graph that is accessible starting from a given node
    :param graph: a cfg graph
    :param number_node: the starting step
    :return: dictionary : a sub-cfg graph
    """
    return {key: graph[key] for key in get_children(number_node, graph) if key != 0}


def get_all_conditions_from_graph(graph):
    """
    :param graph: a cfg graph
    :return: returns a dictionary {node_number: list(conditions)}
    """
    conditions = {}
    for node, value in graph.items():
        if value[0] == 'if' or value[0] == 'while':
            conditions[node] = get_conditions_from_bool_expression(value[1])

    return conditions


def get_all_def(graph):
    """
    Returns a list of step that are assignments (definition) in a CFG
    :param graph: a CFG graph
    :return: list: a list of steps [1, 4]
    """
    variables = get_all_var(graph)
    steps = []
    for variable in variables:
        steps.extend(get_definition_for_variable(graph, variable))

    return steps


def get_definition_for_variable(graph, variable):
    """
    Returns a list of step that are assignments (definition) in a CFG for a given variable
    :param graph: a CFG graph
    :param variable: a variable 'x'
    :return: list: a list of steps [1, 4]
    """
    steps = []
    for key, value in graph.items():
        if is_def(value, variable):
            steps.append(key)
    return steps


def get_utilization_for_variable(graph, variable):
    """
    Returns a list of steps that are utilization (boolean expression or utilization in assignment)
    in a CFG for a given variable
    :param graph: a CFG graph
    :param variable: a variable 'x'
    :return: list: a list of steps [1, 4]
    """
    steps = []
    for key, value in graph.items():
        if is_ref(value, variable):
            steps.append(key)
    return steps


def get_all_var(graph):
    """
    Returns the list of variable assigned/used in a program from a given CFG
    :param graph: a CFG graph
    :return: list: the list of variables ['e', 'r']
    """
    variables = []
    for node, value in graph.items():
        if any(value[0] == x for x in ('while', 'if')):
            variables.extend(get_var_from_bool_expr(value[1]))
        if value[0] == 'assign':
            variables.extend(list(value[1].keys()))

    return variables


def is_def(value_node, variable):
    """
    Check if a node is a definition for a given variable
    :param value_node:
    :param variable:
    :return: boolean True if def, else False
    """
    if value_node[0] != 'assign':
        return False

    if variable in value_node[1]:
        return True
    else:
        return False


def is_ref(value_node, variable):
    """
    Check if a node is a reference for a given variable
    :param value_node:
    :param variable:
    :return: boolean True if ref, else False
    """
    if value_node[0] == 'while' or value_node[0] == 'if':
        if variable in get_var_from_bool_expr(value_node[1]):
            return True
        else:
            return False
    elif value_node[0] == 'assign':

        if variable in value_node[1].values():
            return True
        else:
            return False
    else:
        return False


def get_var_from_bool_expr(expression):
    """
    :param expression: A boolean expression in same format as in CFG graph
    :return: a list of variables ['x', 'y', ..]
    """
    variables = []
    for or_expr in expression:
        for condition in or_expr:
            for value in condition[1]:
                if isinstance(value, str):
                    variables.append(value)

    return variables


def is_sub_path_in_path(sub_path, path):
    """
    Function used in advanced criteria tests, in order to check if a shorter path is part of a larger path
    :param sub_path: list of steps [1, 4, 5]
    :param path: list of steps [1, 4, 5, 6, 8]
    :return: boolean : True if sub path, else False
    """
    if all(step in path for step in sub_path):
        return True
    else:
        return False


def deep_copy_list_dic(list_dic):
    """
    Copy a list of dictionary by creating a copy of each dic that is inside the list.
    Will be used for using functions that modify the graph in place
    :param list_dic: a list of dictionary
    :return: a copy of this list
    """
    new_list = []
    for dic in list_dic:
        new_list.append(dic.copy())
    return new_list
