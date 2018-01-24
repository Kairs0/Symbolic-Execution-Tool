from astToCfg import astToCfg, childrenAreCstOrVar
from asttree import Node

def create_prog_tree():
    tree_prog = Node("sequence")

    # Sequence 1 : if1
    if1 = Node("if")

    # condition if1
    compare1 = Node("compare", "<=")
    var1 = Node("variable", "X")
    cst1 = Node("constant", 0)
    compare1.add_child(var1)
    compare1.add_child(cst1)
    if1.add_child(compare1)

    # if body if1
    assign1 = Node("assign")
    var1 = Node("variable", "X")
    op1 = Node("operation", "-")
    cst2 = Node("constant", 0)
    var2 = Node("variable", "X")
    op1.add_child(cst2)
    op1.add_child(var2)
    assign1.add_child(var1)
    assign1.add_child(op1)
    if1.add_child(assign1)

    # else body if1
    assign2 = Node("assign")
    var3 = Node("variable", "X")
    op2 = Node("operation", "-")
    cst3 = Node("constant", 1)
    var4 = Node("variable", "X")
    op2.add_child(cst3)
    op2.add_child(var4)
    assign2.add_child(var3)
    assign2.add_child(op2)
    if1.add_child(assign2)

    # end seq 1
    tree_prog.add_child(if1)

    # seq 2 : if2
    if2 = Node("if")

    # condition if2
    compare2 = Node("compare", "==")
    var5 = Node("variable", "X")
    cst4 = Node("constant", 1)
    compare2.add_child(var5)
    compare2.add_child(cst4)
    if2.add_child(compare2)

    # if body if2
    assign3 = Node("assign")
    var6 = Node("variable", "X")
    cst5 = Node("constant", 1)
    assign3.add_child(var6)
    assign3.add_child(cst5)
    if2.add_child(assign3)

    # else body if2
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

    # end seq2
    tree_prog.add_child(if2)

    return tree_prog

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

    # ifTree = create_if_cfg()
    # print(str(childrenAreCstOrVar(ifTree)))
    # bodyPart = ifTree.children[1]
    # elsePart = ifTree.children[2]
    # print(str(childrenAreCstOrVar(bodyPart)))

    # parser = astToCfg(ifTree)

    # print(parser.treat_compare_node(ifTree.children[0]))

    # print(parser.treat_operation_node(elsePart.children[1]))

    # print(parser.treat_assign_node(elsePart))

    # print(parser.treat_if_node(ifTree))

    prog_tree = create_prog_tree()

    parser2 = astToCfg(prog_tree)

    print(parser2.treat_seq_node(prog_tree))


