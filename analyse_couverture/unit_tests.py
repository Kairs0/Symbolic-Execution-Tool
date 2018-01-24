from astToCfg import astToCfg, childrenAreCstOrVar
from asttree import Node


def create_if_cfg():
    if2 = Node("if")
    # condition if
    compare2 = Node("compare", "==")
    var5 = Node("variable", "X")
    cst4 = Node("constant", 1)
    compare2.add_child(var5)
    compare2.add_child(cst4)
    if2.add_child(compare2)
    # if body if
    assign3 = Node("assign")
    var6 = Node("variable", "X")
    cst5 = Node("constant", 1)
    assign3.add_child(var6)
    assign3.add_child(cst5)
    if2.add_child(assign3)
    # else body if
    assign4 = Node("assign")
    var7 = Node("variable", "X")
    op3 = Node("operation", "+")
    var8 = Node("variable", "X")
    cst6 = Node("constant", 1)
    op3.add_child(var8)
    op3.add_child(cst6)
    assign4.add_child(var7)
    assign4.add_child(op3)
    if2.add_child(assign4)

    return if2



if __name__ == "__main__":

    ifTree = create_if_cfg()
    print(str(childrenAreCstOrVar(ifTree)))
    bodyPart = ifTree.children[1]
    elsePart = ifTree.children[2]
    print(str(childrenAreCstOrVar(bodyPart)))

    parser = astToCfg(ifTree)

    print(parser.treat_compare_node(ifTree.children[0]))

    print(parser.treat_operation_node(elsePart.children[1]))

    print(parser.treat_assign_node(elsePart))

    print(parser.treat_if_node(ifTree))


