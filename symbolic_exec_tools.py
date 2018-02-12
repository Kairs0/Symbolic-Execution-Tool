from constraint import *
from process_cfg_tools import get_all_var, type_node, is_boolean_expression_node


def is_assign_predicate(step):
    # TODO : ! set spaces between all operators in paths
    if ' = ' in step:
        return True
    else:
        return False


def is_bool_predicate(step):
    return not is_assign_predicate(step)


def get_variable_from_assign_predicate(step):
    return step.split(' = ')[0].replace(' ', '')


def get_variable_from_bool_predicate(step):
    comparators = ['==', '<=', '<', '>', '>=', '!=']
    separator = '=='
    step = step.replace('(', '').replace(')', '')
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


def clean_path_predicate(predicate_path):
    # ['(x1<=0)', 'x2=0-x1', '(x4==1)'] => ['(x4==1)', 'x2=0-x1', '(x1<=0)']
    # => ['(x2==1)', 'x2=0-x1', '(x1<=0)']
    reversed_predicate_path = list(reversed(predicate_path))
    output = []
    for index, step in enumerate(reversed_predicate_path):
        if is_bool_predicate(step):
            var = get_variable_from_bool_predicate(step)
            value_next = get_next_occurrence_variable(reversed_predicate_path[index + 1:], var[0])
            if value_next is not None:
                # replace its value by next variable that has same first letter
                step = step.replace(var.replace(' ', ''), value_next)
        output.append(step)
    return output


def get_variables_from_predicate(predicate_path):
    variables = []
    for step in predicate_path:
        if is_assign_predicate(step):
            variables.append(get_variable_from_assign_predicate(step))
        elif is_bool_predicate(step):
            variables.append(get_variable_from_bool_predicate(step))
    return variables


def solve_path_predicate(predicate_path):
    """
    :param predicate_path:
    :return:
    """
    problem = Problem()
    # si on a une expression booléenne, il faut donner une relation d'égalité entre la variable isolée
    # et la dernière assignation
    clean_path = clean_path_predicate(predicate_path)
    variables = set(get_variables_from_predicate(clean_path))

    for var in variables:
        problem.addVariable(var, range(-10, 10))

    str_add_cs = 'problem.addConstraint(lambda ' + ','.join(variables) + ':'

    # ['(x2 == 1)', 'x2 = 0-x1', '(x1 <= 0)']
    for step in clean_path:
        if is_assign_predicate(step):
            step = step.replace('=', '==')
        exec(str_add_cs + step + ')')
    return problem.getSolution()


def path_predicate(detailed_steps, graph):
    variables = list(set(get_all_var(graph)))
    order = list(detailed_steps.keys())

    order.sort()

    # voir Cours\IVF\Execsymb\cours6.pdf
    # we do not consider last step (not relevant)
    order.pop()

    result_path_predicate = []

    for step in order:
        if isinstance(detailed_steps[step], dict):
            # assign. For ex: {'x': 'x-1'}
            var = list(detailed_steps[step].keys())[0]
            value = detailed_steps[step][var]
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
    # [[('<=', ['x', 0]), ('>', ['y', 2])], [('<=', ['x', 0]), ('>', ['y', 2])]]
    # don't know if util
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


def old_how_to_get_to_node(node_key, graph):
    path_result = [[node_key]]
    current_node = node_key

    previous_nodes = get_father_for_node(current_node, graph)
    while previous_nodes:
        choice_to_get_up = [node for node in previous_nodes if node not in path_result][0]
        if is_boolean_expression_node(graph[choice_to_get_up]):
            if graph[choice_to_get_up][-1][0] in path_result:
                path_result.append([choice_to_get_up, True])
            elif graph[choice_to_get_up][-1][1] in path_result:
                path_result.append([choice_to_get_up, False])
        else:
            path_result.append([choice_to_get_up])
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
