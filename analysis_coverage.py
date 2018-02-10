#!/usr/bin/env python
# -*- coding: utf-8 -*-

from process_cfg_tools import *


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
        if path[:k] in target_paths:
            target_paths.remove(path[:k])

    if len(target_paths) == 0:
        print("All k paths for k = " + str(k) + ": OK")
    else:
        print("All k paths for k = " + str(k) + " fails:")
        print("Paths " + str(target_paths) + " were never taken entirely.")


def all_i_loops(values_test, graph, k):
    # interpretation: for every test value, every loop must be visited at must i times.
    # todo: redefine for inner loops
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
    # there is a path from the affection to its utilization.

    # first : we get all step corresponding to definition, and all steps corresponding to utilization
    # for each variable
    variables_prog = get_all_var(graph)
    steps_per_var = {variable: get_definition_for_variable(graph, variable) for variable in variables_prog}

    for variable in variables_prog:
        steps_per_var[variable] += get_utilization_for_variable(graph, variable)
        steps_per_var[variable] = list(set(steps_per_var[variable]))  # remove duplicates

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
    print("\n ------")
    print("Criterion: all du-paths")
    # interpretation: for each variable, for each couple definition-utilization, all simple path
    # without redefinition of variable are executed one time

    # first: for all variable, find all definition
    variables_prog = get_all_var(graph)
    dic_var_def = {variable: get_definition_for_variable(graph, variable) for variable in variables_prog}

    # second: for all variable, for all its definition, find the first utilization
    # (without definition in the step), and build a list of couples (start-end) that must be reached.
    couple_of_interest = []
    for variable in variables_prog:
        for step_definition in dic_var_def[variable]:
            reachable_graph = get_accessible_graph(graph, step_definition)
            # print(reachable_graph)
            steps_redefine = get_definition_for_variable(reachable_graph, variable)
            steps_utilization = get_utilization_for_variable(reachable_graph, variable)

            # If step_redefine is empty or if first element of utilization is
            # smaller than first element of utilization then we add the couple.
            # In any other case we do not add the couple to couple of interests
            try:
                if (
                        len(steps_redefine) == 0 and len(steps_utilization) > 0 or
                        steps_utilization[0] < steps_redefine[0]
                ):
                    couple_of_interest.append((step_definition, steps_utilization[0]))
            except IndexError:
                pass

    # third: build a list of nodes that are inside while loops
    inside_while_loops_steps = []
    for value in graph.values():
        if type_node(value) == 'while':
            inside_while_loops_steps.append(value[-1][0])

    # fourth: process values from the set of tests
    result_paths = []
    for data in values_test:
        path, var = process_value_test(graph, data)
        result_paths.append(path)

    # fifth: check if all path for each couple have been taken
    # check if inner while loops haven't been looped more than one time
    correctness_couples = {couple: False for couple in couple_of_interest}
    correctness_while = {step: True for step in inside_while_loops_steps}
    for path in result_paths:
        for couple in couple_of_interest:
            if is_sub_path_in_path(list(couple), path):
                correctness_couples[couple] = True
        for step_target in correctness_couples.keys():
            if path.count(step_target) > 1:
                correctness_while[step_target] = False

    if (
            all(result_couple for result_couple in correctness_couples.values())
            and all(result_while for result_while in correctness_while.values())
    ):
        correct = True
    else:
        correct = False

    if correct:
        print("TDU: OK")
    else:
        print("TDU: fails")


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
    path_tests = "sets_tests_txt/test.txt"

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

    # todo : make copy of test values (do not read file at each time

    test_values = read_test_file(path_tests)
    all_affectations(test_values, test_two_variables)
    test_values = read_test_file(path_tests)
    all_decisions(test_values, test_two_variables)
    test_values = read_test_file(path_tests)
    all_affectations(test_values, graph_prog)
    test_values = read_test_file(path_tests)
    all_decisions(test_values, graph_prog)
    test_values = read_test_file(path_tests)
    all_k_paths(test_values, graph_prog, 3)
    test_values = read_test_file(path_tests)
    all_k_paths(test_values, graph_prog, 5)
    test_values = read_test_file(path_tests)
    all_k_paths(test_values, test_two_variables, 3)
    test_values = read_test_file(path_tests)
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

    test_values = read_test_file(path_tests)
    all_conditions(test_values, graph_prog)

    test_values = read_test_file(path_tests)
    all_utilization(test_values, graph_prog)

    test_values = read_test_file(path_tests)
    all_du_path(test_values, graph_prog)


if __name__ == '__main__':
    main()
