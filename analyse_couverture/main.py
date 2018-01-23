"""
Structure du CFG Graph:
The graph is a dictionary.
Key is the number of the node
Value is a tuple containing instructions
tuple[0] contains the command type:
it can be "assign", "while", "if" or "skip"

***** For "if" and "while" commands:
tuple[1] is the comparator it can be "<=" to ">="
tuple[2] is a list of values used to operate the
operator given in tuple[1]. If the list is empty,
the first variable will be checked against the 
second variable of the program.
If the list is len 1, the first variable of the program
will be checked against the value given in the list !TODO compare y
If the list is len 2, the first value will be checked 
against the second
tuple[3] contains a tuple of 2 elements.
The first one is the following node when the
statement is true, the second one the following node when the 
statement is false.

***** For "assign" commands:
tuple[1] is the new value of the first variable x
it reads like : x = tuple[1]
tuple[2] is the new value of the second variable y
it reads like y = tuple[2]
tuple[3] is the following node

***** For "skip" commands:
tuple[1] is the following node
"""

graph_prog = {
    1: ("if", "<=", [0], (2, 3)),
    2: ("assign", "-x", "", 4),
    3: ("assign", "1-x", "", 4),
    4: ("if", "==", "1", (5, 6)),
    5: ("assign", "1", "", 0),
    6: ("assign", "x+1", "", 0)
}

graph_prog_test = {
    1: ("if","<=", [0],(2, 3)), # node[0] : type (assign, while, if, skip)
    2: ("assign", "-x","", 4),
    3: ("assign", "1-x","", 4),
    4: ("if","==", [0], (5,6)),
    5: ("assign", "1","", 8),
    6: ("assign", "x+1","", 8),
    7: ("skip", 9),
    8: ("while", "<=", [4], (6, 7)),
    9: ("assign", "x*x","", 0)
}

# TODO: compare between x and y for if and while
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
            if len(node[2]) == 0:
                next_node = comparison(x, y, node[1], node[3][0], node[3][1])
            elif len(node[2]) == 1:
                next_node = comparison(x, int(node[2][0]), node[1], node[3][0], node[3][1])
            elif len(node[2]) == 2:
                next_node = comparison(int(node[2][0]), int(node[2][1]), node[1], node[3][0], node[3][1])
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

    PATH_TESTS = "tests/test.txt"

    valeurs_test = []
    with open(PATH_TESTS) as file:
        for line in file:
            valeurs_test.append(int(line))

    toutes_affectation(valeurs_test, graph_prog)
    toutes_decisions(valeurs_test, graph_prog)




# NOEUD:
# while ou if,
# Arret:
# assing ou skip