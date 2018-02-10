#!/usr/bin/env python
# -*- coding: utf-8 -*-

LIMIT_FOR_INFINITE_LOOP = 100


def process_value_test(graph, variables, info_conditions=False):
    """
    :param graph: CFG graph
    :param variables: a dictionary {var: initial_value}
    :param info_conditions: a boolean, if true: will return an additional value which is a dic,
    stating how each condition was evaluated.
    :return: steps the program went through, dic of final values of variables
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


def type_node(node_value):
    return node_value[0]


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


def process_bool_expression(conditions, variables):
    """

    :param conditions: [[(comp1), (comp2)],[(comp3), (comp4)]], each element is a list of conditions that
    must be respected (and logical gate)
    :param variables:
    :return:
    """
    result = True
    # we want AND between each condition
    # -> if any of the condition is false, the result is false
    if any(not process_or_expression(condition, variables) for condition in conditions):
        result = False

    return result


def process_or_expression(conditions, variables):
    result = False
    # we want a OR between each condition
    # -> if only one condition is true, the result is true
    if any(process_condition(condition, variables) for condition in conditions):
        result = True

    return result


def process_condition(comparison, variables):
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


def compare(operator, a, b):
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


def get_all_paths(graph, start, path=None):
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


def replace_any_var_by_value(instruction, variables):
    for key, value in variables.items():
        instruction = instruction.replace(key, str(value))
    return instruction


def get_following_nodes(node_value):
    return node_value[-1]


def get_children(step_number, graph, visited=None):
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
    :param graph:
    :param number_node:
    :return: dictionary
    """
    return {key: graph[key] for key in get_children(number_node, graph) if key != 0}


def get_all_conditions_from_graph(graph):
    """
    :param graph:
    :return: returns a dictionary {node: list(conditions)}
    """
    conditions = {}
    for node, value in graph.items():
        if value[0] == 'if' or value[0] == 'while':
            conditions[node] = get_conditions_from_bool_expression(value[1])

    return conditions


def get_conditions_from_bool_expression(boolean_expression):
    """
    :param boolean_expression: simple: [[('<=', ['x', 0])]]
    and: [[('<=', ['x', 0])], [('>', ['y', 2])]]
    or: [[('<=', ['x', 0]), ('>', ['y', 2])]]
    complex: [[('<=', ['x', 0]), ('>', ['y', 2])], [('<=', ['x', 0]), ('>', ['y', 2])]]
    :return: list of conditions, without any structure to distinguish between and/or
    """
    conditions = []
    for expressions in boolean_expression:
        for condition in expressions:
            conditions.append(condition)

    return conditions


def get_all_def(graph):
    """
    Returns a list of step that are assignments (definition) in a CFG
    :param graph:
    :return: list
    """
    variables = get_all_var(graph)
    steps = []
    for variable in variables:
        steps.extend(get_definition_for_variable(graph, variable))

    return steps


def get_definition_for_variable(graph, variable):
    """
    Returns a list of step that are assignments (definition) in a CFG for a given variable
    :param graph:
    :param variable:
    :return: list
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
    :param graph:
    :param variable:
    :return: list
    """
    steps = []
    for key, value in graph.items():
        if is_ref(value, variable):
            steps.append(key)
    return steps


def get_all_var(graph):
    """
    returns the list of variable assigned/used in a program from a given CFG
    :param graph:
    :return: list
    """
    variables = []
    for node, value in graph.items():
        if any(value[0] == x for x in ('while', 'if')):
            variables.extend(get_var_from_bool_expr(value[1]))
        if value[0] == 'assign':
            variables.extend(list(value[1].keys()))

    return variables


def is_def(value_node, variable):
    if value_node[0] != 'assign':
        return False

    if variable in value_node[1]:
        return True
    else:
        return False


def is_ref(value_node, variable):
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
    variables = []
    for or_expr in expression:
        for condition in or_expr:
            for value in condition[1]:
                if isinstance(value, str):
                    variables.append(value)

    return variables


def all_affectations(values_test, graph):
    print("\n ------")
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
    print("\n ------")
    print("Criterion: all decisions")

    objective = []
    for key, value in graph.items():
        if value[0] == "if" or value[0] == "while":
            objective.append(key)
            for following_nodes in value[-1]:
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


def all_k_paths(values_test, graph, k):
    print("\n ------")
    print("Criterion: all k paths for k = " + str(k))

    all_paths = get_all_paths(graph, 1)

    target_paths = []
    for path in all_paths:
        if not path[:k] in target_paths:
            target_paths.append(path[:k])

    print("We want the following paths to be taken: " + str(target_paths))

    for value in values_test:
        path, var = process_value_test(graph, value)
        # print("path for value " + str(value) + " : " + str(path))
        if path[:k] in target_paths:
            target_paths.remove(path[:k])

    if len(target_paths) == 0:
        print("All k paths for k = " + str(k) + ": OK")
    else:
        print("All k paths for k = " + str(k) + " fails:")
        print("Paths " + str(target_paths) + " were never taken entirely.")


def all_i_loops(values_test, graph, k):
    # interpretation: for every test value, the loop must be visited at must i times.
    print("\n ------")
    print("Criterion: all i loops")

    objective = []
    for key, value in graph.items():
        if value[0] == "while":
            objective.append(value[-1][0])

    print("We want the following nodes " + str(objective) + " to be visited. (At must " + str(k) + " times.)")

    count_dic = {obj: 0 for obj in objective}
    results = {str(data): count_dic.copy() for data in values_test}

    for data in values_test:
        # make a string copy of data in order to retrieve in result the count dictionary corresponding
        # (value dictionary dic is modified while data is processed
        str_data = str(data)
        path, var = process_value_test(graph, data)
        for step in path:
            if step in objective:
                results[str_data][step] += 1

    correct = True
    for result in results.values():
        if not all(k >= value > 0 for value in result.values()):
            correct = False

    if correct:
        print(str(k) + "-TB: OK")
    else:
        print(str(k) + "-TB fails:")


def all_definitions(values_test, graph):
    print("\n ------")
    print("Criterion: all definitions")

    # interpretation : for every variable, for every definition,
    # todo: change (we must have at least one variable in the test that respects the condition, and not every
    # there is a path from the affection to its utilization.

    # first : we get all step corresponding to definition, and all steps corresponding to utilization
    # for each variable
    variables_prog = get_all_var(graph)
    steps_per_var = {variable: get_definition_for_variable(graph, variable) for variable in variables_prog}

    for variable in variables_prog:
        steps_per_var[variable] += get_utilization_for_variable(graph, variable)
        steps_per_var[variable] = list(set(steps_per_var[variable]))  # dirty way to remove duplicates

    result = {variable: False for variable in variables_prog}

    print("for following variables, we want the corresponding path to be taken: ")
    print(steps_per_var)

    # for each variable, if for a data test a variable is assigned, then this variable must be used.
    for value in values_test:
        for var in variables_prog:
            values_to_process = value.copy()  # we process a copy
            # of the value dic so that the value of dic is not be modified
            step_to_follow = steps_per_var[var]
            path, result_vars = process_value_test(graph, values_to_process)
            for step in path:
                if step in step_to_follow:
                    step_to_follow.remove(step)
            if len(step_to_follow) == 0:
                result[var] = True

    # if any(valid for valid in result.values()): # todo new condition
    if all(valid for valid in result.values()):
        print("TDef: OK")
    else:
        print("TDef: fails")


def is_sub_path_in_path(sub_path, path):
    if all(step in path for step in sub_path):
        return True
    else:
        return False


def all_utilization(values_test, graph):
    print("\n ------")
    print("Criterion: all utilization")
    # interpretation: for each variable, after all definition, the path that leads to the utilization
    # following the definition is taken (difference with former criteria: that the path leading to its execution)

    variables_prog = get_all_var(graph)

    # first: get each definition
    dic_var_def = {variable: get_definition_for_variable(graph, variable) for variable in variables_prog}

    # second: get all utilization accessible from each definition
    targets_paths = {}
    count_path = 0
    for var in variables_prog:
        for step_definition in dic_var_def[var]:
            targets_paths[count_path] = [step_definition]
            reachable_graph = get_accessible_graph(graph, step_definition)
            steps_utilization = get_utilization_for_variable(reachable_graph, var)
            targets_paths[count_path] += steps_utilization
            count_path += 1

    # third : process value test and record the resulting path
    result_paths = []
    for data in values_test:
        path, var = process_value_test(graph, data)
        result_paths.append(path)

    # fourth: validate targets path that have been taken
    validated = []
    for target_path in targets_paths.values():
        for path_result in result_paths:
            if is_sub_path_in_path(target_path, path_result):
                validated.append(target_path)

    # fifth: test results
    targets_paths_list = [path for path in targets_paths.values()]

    if set(map(tuple, validated)) == set(map(tuple, targets_paths_list)):
        print("TU: Ok")
    else:
        print("TU: fails")


def all_du_path(values_test, graph):
    # todo
    pass


def all_conditions(values_test, graph):
    print("\n ------")
    print("Criterion: all conditions")

    # dictionary {node: list(conditions)}
    conditions = get_all_conditions_from_graph(graph)

    result_true = {str(condition): False for condition in conditions.values()}
    result_false = result_true.copy()

    # when a condition is evaluated to true in the program, we set its value to
    # true in result_true. When it's evaluated to false, we set its value to false in result_false.

    for value in values_test:
        path, var, info_cond = process_value_test(graph, value, info_conditions=True)
        # info cond: a dic {node: list(evaluated conditions)
        for index_node, list_results in info_cond.items():
            for index, result in enumerate(list_results):
                condition_just_evaluated = conditions[index_node][index]
                if result:
                    result_true[str([condition_just_evaluated])] = True
                else:
                    result_false[str([condition_just_evaluated])] = True

    if all(correct for correct in result_true.values()) and all(correct for correct in result_false.values()):
        print("TC: OK")
    else:
        print("TC: fails")


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


def main():
    PATH_TESTS = "sets_tests_txt/test.txt"

    # Hand written CFG graphs
    # (temporary - while ast_to_cfg isn't connected to process_tests)

    test_two_variables = {
        1: ['if', [[('<=', ['x', 0])]], [2, 3]],
        2: ['assign', {'y': 'x'}, [4]],
        3: ['assign', {'y': '0-x'}, [4]],
        4: ['assign', {'x': 'y*2'}, [0]]
    }

    graph_prog = {
        1: ['if', [[('<=', ["x", 0])]], [2, 3]],
        2: ['assign', {'x': '0-x'}, [4]],
        3: ['assign', {'x': '1-x'}, [4]],
        4: ['if', [[('==', ["x", 1])]], [5, 6]],
        5: ['assign', {'x': '1'}, [0]],
        6: ['assign', {'x': 'x+1'}, [0]]
    }

    graph_factorial = {
        1: ['assign', {'n': '1'}, [2]],
        2: ['while', [[('>=', ['x', 1])]], [3, 0]],
        3: ['assign', {'n': 'n*x'}, [4]],
        4: ['assign', {'x': 'x-1'}, [2]]
    }

    test_values = read_test_file(PATH_TESTS)
    all_affectations(test_values, test_two_variables)
    test_values = read_test_file(PATH_TESTS)
    all_decisions(test_values, test_two_variables)
    test_values = read_test_file(PATH_TESTS)
    all_affectations(test_values, graph_prog)
    test_values = read_test_file(PATH_TESTS)
    all_decisions(test_values, graph_prog)
    test_values = read_test_file(PATH_TESTS)
    all_k_paths(test_values, graph_prog, 3)
    test_values = read_test_file(PATH_TESTS)
    all_k_paths(test_values, graph_prog, 5)
    test_values = read_test_file(PATH_TESTS)
    all_k_paths(test_values, test_two_variables, 3)
    test_values = read_test_file(PATH_TESTS)
    all_k_paths(test_values, test_two_variables, 5)

    test_values = read_test_file("sets_tests_txt/tests_for_fact.txt")
    all_affectations(test_values, graph_factorial)

    test_values = read_test_file("sets_tests_txt/tests_for_fact.txt")
    all_i_loops(test_values, graph_factorial, 2)

    test_values = read_test_file('sets_tests_txt/tests2.txt')
    all_i_loops(test_values, graph_factorial, 2)

    test_values = read_test_file('sets_tests_txt/tests_for_fact.txt')
    all_definitions(test_values, graph_factorial)

    test_values = read_test_file('sets_tests_txt/tests_for_fact.txt')
    all_conditions(test_values, graph_factorial)

    test_values = read_test_file(PATH_TESTS)
    all_conditions(test_values, test_two_variables)

    test_values = read_test_file(PATH_TESTS)
    all_utilization(test_values, test_two_variables)


if __name__ == '__main__':
    main()
