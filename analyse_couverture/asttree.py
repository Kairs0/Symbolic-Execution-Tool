"""
#### AST Tree structure:

# Each node has a category (string), values can be : 
sequence, if, variable, constant, operation, assign, compare TODO: WHILE

# Each node has a list of nodes which are his children

# A node can have a data (for constant, operation, compare, variable)
constant: data is the value of the constant,
variable: data is the name of the variable
compare : data is the operator (==, <=, ...)
operation: data is the operator (+, *, ...)

"""


class Node(object):
    def __init__(self, category, data=None):
        self.data = data
        self.category = category
        self.children = []
        self.level = 0

    def add_child(self, obj):
        self.children.append(obj)

    def calc_level(self):
        rec_calc_level(self, 0)

    def get_height(self):
        self.calc_level()
        h = 0
        for n in get_all_nodes_and_leaves(self):
            if n.level > h:
                h = n.level

        return h

    def print_me(self):
        h = self.get_height()
        tree_list = get_all_nodes_and_leaves(self)
        to_print = []
        for i in range(h):
            to_print.append([])
            for node in tree_list:
                if node.level == i:
                    to_print[i].append(node)

        for nodes_list in to_print:
            for node in nodes_list:
                print(node.category, end='-')
            print("\n|")


def get_all_nodes_and_leaves(node):
    result = [node]
    if len(node.children) == 0:
        return result
    else:
        for child in node.children:
            result = result + get_all_nodes_and_leaves(child)
    return result


def rec_calc_level(node, lvl):
    node.level = lvl
    for child in node.children:
        rec_calc_level(child, lvl + 1)


class GeneratorAstTree(object):

    @staticmethod
    def create_prog_tree():
        """
        The prog program (from subject) implemented with our tree
        """
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

    @staticmethod
    def create_if_cfg():
        """
        Creates a basic if node
        """
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

    @staticmethod
    def create_if_cfg_else_is_seq():
        """
        Creates a if node in which the else part contains a sequence
        """
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
        seq = Node("sequence")
        # 1 assign
        assign4 = Node("assign")
        var7 = Node("variable", "X")
        cst8 = Node("constant", 32)
        assign4.add_child(var7)
        assign4.add_child(cst8)
        seq.add_child(assign4)

        # 2 assign
        assign5 = Node("assign")
        var8 = Node("variable", "X")
        op = Node("operation", "*")
        var9 = Node("variable", "X")
        cst9 = Node("constant", 4)
        op.add_child(var9)
        op.add_child(cst9)
        assign5.add_child(var8)
        assign5.add_child(op)
        seq.add_child(assign5)

        if2.add_child(seq)
        return if2
