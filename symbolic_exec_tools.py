from constraint import *
from process_cfg_tools import get_all_var, type_node, is_boolean_expression_node
import re


def generate_value_from_node(graph, target):
    path = path_to_node(target, graph)
    detailed_path = detailed_steps_path(path, graph)
    predicate = path_predicate(detailed_path, graph)
    solution = solve_path_predicate(predicate)
    if solution is not None:
        return clean_solution(solution)
    else:
        return {}


def generate_value_from_path(graph, target_path):
    target_path.reverse()
    detailed_path = detailed_steps_path(target_path, graph)
    predicate = path_predicate(detailed_path, graph)
    solution = solve_path_predicate(predicate)
    if solution is not None:
        return clean_solution(solution)
    else:
        return {}


def clean_solution(solution):
    # {'x1': 0, 'x2': 0}
    key_values_solution = []
    for key in solution:
        if key[1] == '1':
            key_values_solution.append(key)
    cleaned_solution = {key[0]: solution[key] for key in key_values_solution}
    return cleaned_solution


def is_assign_predicate(step):
    if ' = ' in step:
        return True
    else:
        return False


def is_bool_predicate(step):
    return not is_assign_predicate(step)


def split(txt, separators):
    """
    Split a string using a list of separators
    :param txt: a string
    :param separators: a list of separators
    :return: the list of string, split
    """
    default_sep = separators[0]

    # skip seps[0] because that's the default separator
    for sep in separators[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def str_represents_number(test_string):
    try:
        # noinspection PyListCreation
        float(test_string)
        return True
    except ValueError:
        return False


def get_variable_from_assign_predicate(step):
    """
    'x2 = 1'
    'x3 = 1 - x2'
    :param step:
    :return:
    """
    operators = ['+', '-', '*']

    # add first var (before the assign)
    result = [step.split(' = ')[0].replace(' ', '')]

    maybe_vars = split(step.split(' = ')[1].replace(' ', ''), operators)

    for potential_var in maybe_vars:
        if not str_represents_number(potential_var):
            result.append(potential_var)

    return result


def get_variable_from_bool_predicate(step):
    # (x1 <= 0)
    # not ((x1 <= 0))
    comparators = ['==', '<=', '<', '>', '>=', '!=']
    separator = '=='
    step = step.replace('(', '').replace(')', '').replace('not', '')
    for comparator in comparators:
        if comparator in step:
            separator = comparator
    # TODO works only on bool value such as x1 == 2 or x1 <= 3!!!!!
    return step.split(separator)[0].replace(' ', '')


def get_next_occurrence_variable(predicate_path, variable):
    for step in predicate_path:
        if variable in step:
            index_var = step.index(variable)
            return step[index_var:index_var + 2]


def get_variables_from_predicate(predicate_path):
    variables = []
    for step in predicate_path:
        if is_assign_predicate(step):
            variables.extend(get_variable_from_assign_predicate(step))
        elif is_bool_predicate(step):
            variables.append(get_variable_from_bool_predicate(step))
    return variables


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    Util made in order to sort a list of string + number following the numbers.
    list.sort(key=natural_keys) : sorts in human order
    source
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [atoi(c) for c in re.split('(\d+)', text)]


def order_var(set_variables):
    """
    From a set of variables + number step ('x1', 'x4', 'y1', 'y6'), organize by variable name ('x', 'y'
    and for each variable order the set
    :param set_variables: a set of variables + steps {'x1', 'x4', 'y1'}
    :return: a dictionary {variable: order variable } {'x': ['x1', 'x3', 'x4']}
    """
    dic_res = {}
    for var in set_variables:
        name_var = var[0]  # 'x'
        if name_var not in dic_res.keys():
            dic_res[name_var] = [var]
        else:
            dic_res[name_var].append(var)
    # in each value of dic, we order variable by order x1=>x2=>x4
    for value in dic_res.values():
        value.sort(key=natural_keys)
    return dic_res


def organization_in_couple(dic_organization_var):
    """
    make couple of variable
    :param dic_organization_var: a dic of variable: variable + step ordered
    :return: a list of couples [['x1', 'x2'], ['y1', 'y2']]
    """
    # input: a dic {'x':['x1', ...], 'y' : ['y3', 'y5', ...]}

    result = []
    for key, value in dic_organization_var.items():
        for i in range(len(value) - 1):
            result.append([value[i], value[i+1]])

    # output a list of couple [('x1', 'x3'), ('y1', 'y4')] to set equal
    return result


def check_auto_reference(predicate_path):
    list_auto_references = []
    for step in predicate_path:
        if not is_bool_predicate(step):
            variables = get_variable_from_assign_predicate(step)
            # assume that variables are ordered and variables[0] is the variable that is being assigned.
            array_type_var = [var[0] for var in variables]
            # if first variable (the one that is assigned) is inside
            # the rest of variable, variables are auto assigned
            if variables[0][0] in array_type_var[1:]:
                for referenced_variable in variables[1:]:
                    if variables[0][0] in referenced_variable:
                        list_auto_references.append([variables[0], referenced_variable])
    return list_auto_references


def couples_equals(predicate_path_reversed, couples_variables):
    couple_auto_ref = check_auto_reference(predicate_path_reversed)
    couple_auto_ref2 = couple_auto_ref.copy()
    for couple in couple_auto_ref2:
        couple.reverse()
    couple_to_stick_together = [couple for couple in couples_variables if couple not in couple_auto_ref]
    if couple_auto_ref2 is not None:
        couple_to_stick_together = [couple for couple in couple_to_stick_together if couple not in couple_auto_ref2]
    return couple_to_stick_together


def solve_path_predicate(predicate_path):
    """
    :param predicate_path:
    :return:
    """
    problem = Problem()

    predicate_path.reverse()

    variables = set(get_variables_from_predicate(predicate_path))

    dic_ordered_variables = order_var(variables)
    couples_variables = organization_in_couple(dic_ordered_variables)

    # if only one variable, we add an useless and arbitrary variable in order to be able to write
    # functioning lambda functions. indeed, python constraint api seems to be written in python 2.x
    # and calling solution over a constraint defined with only one variable returns an error 'TypeError'
    # which seems to come from dic.keys() which returned a list in py 2.x. With python3.x, d.keys()
    # returns a dict_keys.
    if len(variables) == 1:
        variables.add('pp')

    for var in variables:
        problem.addVariable(var, range(-50, 50))

    str_add_cs = 'problem.addConstraint(lambda ' + ','.join(variables) + ':'

    # equality between all variables following themselves (x1 == x2 , x3 == x4),
    # except for variables that are assigned (assign : 'x2 = - x1' -> x2 !=x1)
    couples_to_stick_together = couples_equals(predicate_path, couples_variables)
    for couple_var in couples_to_stick_together:
        to_add = couple_var[0] + '==' + couple_var[1]
        exec(str_add_cs + to_add + ')')

    # ['(x2 == 1)', 'x2 = 0-x1', '(x1 <= 0)']
    for step in predicate_path:
        if is_assign_predicate(step):
            step = step.replace('=', '==')

        exec(str_add_cs + step + ')')

    return problem.getSolution()


def path_predicate(detailed_steps, graph):
    variables = list(set(get_all_var(graph)))
    order = list(detailed_steps.keys())

    order.sort()

    # we do not consider last step (not relevant)
    order.pop()

    result_path_predicate = []

    for step in order:
        if isinstance(detailed_steps[step], dict):
            # assign. For ex: {'x': 'x-1'}
            var = list(detailed_steps[step].keys())[0]
            value = detailed_steps[step][var]
            # todo: here, in value, replace any symbol operation (+, -, *) that is not spaced out by a space
            # process value (eg replace each occurrence of variable 'x' by its value at step 'x8')
            for variable in variables:
                if variable in value:
                    value = value.replace(variable, variable + str(step-1))
            # value_processed = value
            result_path_predicate.append(
                var + str(step) + ' = ' + value
            )
        elif isinstance(detailed_steps[step], list):
            # boolean expression and its  [[[('<=', ["x", 0])]], False]
            bool_expr_str = transform_bool_expr_to_str(detailed_steps[step][0])
            if not detailed_steps[step][1]:
                bool_expr_str = 'not (' + bool_expr_str + ')'

            for variable in variables:
                if variable in bool_expr_str:
                    bool_expr_str = bool_expr_str.replace(variable, variable + str(step))

            result_path_predicate.append(
                bool_expr_str
            )

    return result_path_predicate


def transform_bool_expr_to_str(boolean_expression):
    """
    From a structured boolean expression (from CFG graph) returns its equivalent in str
    :param boolean_expression: eg [[('<=', ['x', 0]), ('>', ['y', 2])], [('<=', ['x', 0]), ('>', ['y', 2])]]
    :return: str (boolean expression)
    """
    and_str_list = []
    for and_expr in boolean_expression:
        or_str_list = []
        for or_expr in and_expr:
            or_str = str(or_expr[1][0]) + ' ' + or_expr[0] + ' ' + str(or_expr[1][1])
            or_str_list.append(or_str)
        full_or_str = " or ".join(or_str_list)
        and_str = '(' + full_or_str + ')'
        and_str_list.append(and_str)
    full_and_str = " and ".join(and_str_list)
    return full_and_str


def detailed_steps_path(path, graph):
    result = {}
    for index, step in enumerate(path):
        if type_node(graph[step]) == 'assign':
            result[step] = graph[step][1]
        elif is_boolean_expression_node(graph[step]):
            result[step] = [graph[step][1]]
            if graph[step][-1][0] == path[index - 1]:
                result[step].append(True)
            elif graph[step][-1][1] == path[index - 1]:
                result[step].append(False)
    return result


def path_to_node(node_key, graph):
    path_result = [node_key]
    current_node = node_key

    previous_nodes = get_father_for_node(current_node, graph)
    while previous_nodes:
        choice_to_get_up = [node for node in previous_nodes if node not in path_result][0]
        path_result.append(choice_to_get_up)
        previous_nodes = get_father_for_node(choice_to_get_up, graph)

    return path_result


def get_father_for_node(node_key, graph):
    """
    Returns list of nodes that precede given node
    :param node_key:
    :param graph:
    :return:
    """
    result = []
    for key, value in graph.items():
        if node_key in value[-1]:
            result.append(key)

    return result
