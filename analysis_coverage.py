#!/usr/bin/env python
# -*- coding: utf-8 -*-

from process_cfg_tools import *
from sys import argv, exit
import my_parser
from ast_tree import GeneratorAstTree
from ast_to_cfg import AstToCfgConverter


def all_affectations(values_test, graph, verbose):
    if verbose:
        print("\n ------")
        print("Criterion: all affectations")

    objective = []
    for key, value in graph.items():
        if value[0] == "assign":
            objective.append(key)

    objective_copy = objective.copy()

    if verbose:
        print("We want the following nodes to be visited: " + str(objective))

    for value in values_test:
        path, var = process_value_test(graph, value)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        if verbose:
            print("TA: OK")
            print("Coverage: 100%")
        return True
    else:
        if verbose:
            print("TA fails:")
            print("Nodes " + str(objective) + " were never reached.")
            coverage = round((len(objective_copy) - len(objective)) / len(objective_copy), 4) * 100
            print("Coverage: " + str(coverage) + "%")
        return False


def all_decisions(values_test, graph, verbose):
    if verbose:
        print("\n ------")
        print("Criterion: all decisions")

    objective = []
    for key, value in graph.items():
        if value[0] == "if" or value[0] == "while":
            objective.append(key)
            for following_nodes in value[-1]:
                objective.append(following_nodes)

    objective_copy = objective.copy()

    if verbose:
        print("We want the following nodes to be visited: " + str(objective))

    for value in values_test:
        path, var = process_value_test(graph, value)
        for step in path:
            if step in objective:
                objective.remove(step)
    
    if len(objective) == 0:
        if verbose:
            print("TD: OK")
            print("Coverage: 100%")
        return True
    else:
        if verbose:
            print("TD fails:")
            print("Nodes " + str(objective) + " were never reached.")
            coverage = round((len(objective_copy) - len(objective)) / len(objective_copy), 4) * 100
            print("Coverage: " + str(coverage) + "%")
        return False


def all_k_paths(values_test, graph, k, verbose):
    if verbose:
        print("\n ------")
        print("Criterion: all k paths for k = " + str(k))

    target_paths = get_all_k_paths_brute(graph, k)
    copy_to_conclusion = target_paths.copy()

    if verbose:
        print("We want the following paths to be taken: " + str(target_paths))

    for value in values_test:
        path, var = process_value_test(graph, value)
        if path[:k] in target_paths:
            target_paths.remove(path[:k])

    if len(target_paths) == 0:
        if verbose:
            print("All k paths for k = " + str(k) + ": OK.")
            print("Coverage 100%")
        return True
    else:
        if verbose:
            print("All k paths for k = " + str(k) + " fails:")
            print("Paths " + str(target_paths) + " were never taken entirely.")
            coverage = round((len(copy_to_conclusion) - len(target_paths)) / len(copy_to_conclusion), 4) * 100
            print("Coverage: " + str(coverage) + " %.")
        return False


def all_i_loops(values_test, graph, k, verbose):
    # interpretation: every loop must be visited at must i times.
    # todo if time allows it: redefine to check for inner loops that are visited multiple time
    if verbose:
        print("\n ------")
        print("Criterion: all i loops")

    objective = []
    for key, value in graph.items():
        if value[0] == "while":
            objective.append(value[-1][0])

    objective_copy = objective.copy()

    if verbose:
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

    for result in results.values():
        for obj, value_result in result.items():
            if k >= value_result > 0:
                if obj in objective:
                    objective.remove(obj)

    if len(objective) == 0:
        if verbose:
            print(str(k) + "-TB: OK")
            print("Coverage: 100 %")
        return True
    else:
        if verbose:
            print(str(k) + "-TB fails:")
            print("Nodes " + str(objective) + " were either not visited too many times or never visited.")
            coverage = round((len(objective_copy) - len(objective)) / len(objective_copy), 4) * 100
            print("Coverage: " + str(coverage) + "%")
        return False


def all_definitions(values_test, graph, verbose):
    if verbose:
        print("\n ------")
        print("Criterion: all definitions")

    # interpretation : for every variable, for every definition,
    # there is a path from the affection to its utilization.

    # first : we get all step corresponding to definition, and all steps corresponding to utilization
    # for each variable
    variables_prog = get_all_var(graph)
    steps_per_var = {variable: get_definition_for_variable(graph, variable) for variable in variables_prog}

    # there could be variable that are never defined. In this case, we remove them from list of variable
    # of interest.
    variables_prog = [key for key, value in steps_per_var.items() if len(value) != 0]

    for variable in variables_prog:
        steps_per_var[variable] += get_utilization_for_variable(graph, variable)
        steps_per_var[variable] = list(set(steps_per_var[variable]))  # remove duplicates

    result = {variable: False for variable in variables_prog}

    if verbose:
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
        if verbose:
            print("TDef: OK")
            print("Coverage: 100 %")
        return True
    else:
        if verbose:
            non_valid_variables = [key for key, valid in result.items() if not valid]
            coverage = round(len(result) - len(non_valid_variables) / len(result), 4) * 100
            print("TDef: fails")
            print("Variables " + str(non_valid_variables) + " were not used.")
            print("Coverage: " + str(coverage) + "%")
        return False


def all_utilization(values_test, graph, verbose):
    if verbose:
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
    # clean target path (we want only couple def - utilization)
    key_to_remove = []
    for key, value in targets_paths.items():
        if len(value) == 1:
            key_to_remove.append(key)
    for key in key_to_remove:
        targets_paths.pop(key)

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
        if verbose:
            print("TU: Ok")
            print("Coverage: 100 %")
        return True
    else:
        if verbose:
            not_validated = [path for path in targets_paths.values() if path not in validated]
            len_not_validated = len(set(map(tuple, not_validated)))

            len_target = len(set(map(tuple, targets_paths_list)))
            coverage = round((len_target - len_not_validated) / len_target, 4) * 100
            print("TU: fails")
            print("Following paths were never taken: " + str(list(set(map(tuple, not_validated)))))
            print("Coverage: " + str(coverage) + "%")
        return False


def all_du_path(values_test, graph, verbose):
    if verbose:
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
        if verbose:
            print("TDU: OK")
            print("Coverage: 100%")
        return True
    else:
        if verbose:
            bad_results = [key for key, result_couple in correctness_couples.items() if not result_couple]
            bad_results.append(
                [key for key, result_while in correctness_while.items() if not result_while]
            )

            nb_bad_result = len(bad_results)

            coverage = round((len(correctness_couples) + len(correctness_while) - nb_bad_result) /
                             (len(correctness_couples) + len(correctness_while)), 4) * 100
            print("TDU: fails")
            print("Following couples definition - utilisation were never taken"
                  "or were executed more than one time: " + str(bad_results))
            print("Coverage: " + str(coverage) + "%")
        return False


def all_conditions(values_test, graph, verbose):
    if verbose:
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
        if verbose:
            print("TC: OK")
            print("Coverage: 100%")
        return True
    else:
        if verbose:
            nb_total_cond = len(result_true) + len(result_false)
            cond_non_valid = [cond for cond, correct in result_true.items() if not correct]
            not_valid_list = [cond for cond, correct in result_false.items() if not correct]
            if len(not_valid_list) != 0:
                cond_non_valid.append(not_valid_list)
            len_non_valid = len(cond_non_valid)
            coverage = round((nb_total_cond - len_non_valid) / nb_total_cond, 4) * 100
            print("TC: fails")
            print("Following conditions were not evaluated entirely: " + str(cond_non_valid))
            print("coverage: " + str(coverage) + "%")
        return False


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


def treat_command():
    try:
        file_program = argv[1]
        file_test = argv[2]
        verbose = False
        if len(argv) == 4:
            verbose = argv[3] == '-v'
        return file_program, file_test, verbose
    except IndexError:
        display_usage()
        exit()


def display_usage():
    print("Usage: ")
    print("$ python analysis_coverage.py path_prog.txt path_data_test.txt [-v]")


def get_name_file_from_path(path):
    return path.split('\\')[-1].split('.')[0]


def calc_coverage(cfg_graph, test_values, verbose):
    print("Starting analysis...")
    number_tests = 8
    copies_values = []
    for i in range(number_tests):
        copies_values.append(deep_copy_list_dic(test_values))

    # noinspection PyListCreation
    results = []
    results.append(all_affectations(copies_values[0], cfg_graph, verbose))
    results.append(all_decisions(copies_values[1], cfg_graph, verbose))
    results.append(all_k_paths(copies_values[2], cfg_graph, 4, verbose))
    results.append(all_i_loops(copies_values[3], cfg_graph, 2, verbose))
    results.append(all_definitions(copies_values[4], cfg_graph, verbose))
    results.append(all_utilization(copies_values[5], cfg_graph, verbose))
    results.append(all_du_path(copies_values[6], cfg_graph, verbose))
    results.append(all_conditions(copies_values[7], cfg_graph, verbose))

    count_pass = 0
    for result in results:
        if result:
            count_pass += 1

    print("End analysis coverage.")

    print("Tests are passing " + str(count_pass) + " criterion on " + str(len(results)))


def main():
    file_program, file_test, verbose = treat_command()
    test_values = read_test_file(file_test)

    # if parser is on, we get the AST Tree by parsing the file program.
    # if not, we get the AST tree already written from ast_tree.py module
    if my_parser.is_on():
        # TODO
        ast_tree_prog = {}
    else:
        name_prog = get_name_file_from_path(file_program)
        ast_tree_prog = GeneratorAstTree.get_ast_from_name(name_prog)

    # Convert AST to CFG
    converter = AstToCfgConverter(ast_tree_prog)
    cfg_graph_prog = converter.get_cfg_graph()

    # Process tests to get coverage
    calc_coverage(cfg_graph_prog, test_values, verbose)


if __name__ == '__main__':
    # python .\analysis_coverage.py .\sources_txt\prog_1.txt .\sets_tests_txt\tests_generated.txt -v
    main()
