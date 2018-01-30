"""
#### AST Tree structure:

# Each node has a category (string), values can be : 
sequence, if, variable, constant, operation, assign, compare, while

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
    def sequence_if_and_assign():
        """
        if X <= 0
            then Y := X
            else Y := -X
        X := 2*Y
        :return: ast tree
        """
        seq = Node("sequence")

        # sequence 1
        if1 = Node("if")
        # condition
        compare = Node("compare", "<=")
        var1 = Node("variable", "x")
        cst1 = Node("constant", 0)
        compare.add_child(var1)
        compare.add_child(cst1)

        # then body
        assign = Node("assign")
        var2 = Node("variable", "y")
        var3 = Node("variable", "x")
        assign.add_child(var2)
        assign.add_child(var3)

        # else body
        assign2 = Node("assign")
        var4 = Node("variable", "y")
        op1 = Node("operation", "-")
        cst2 = Node("constant", 0)
        var5 = Node("variable", "x")
        op1.add_child(cst2)
        op1.add_child(var5)
        assign2.add_child(var4)
        assign2.add_child(op1)

        if1.add_child(compare)
        if1.add_child(assign)
        if1.add_child(assign2)

        # sequence 2
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        op2 = Node("operation", "*")
        var7 = Node("variable", "y")
        cst3 = Node("constant", 2)
        op2.add_child(var7)
        op2.add_child(cst3)
        assign3.add_child(var6)
        assign3.add_child(op2)

        # seq
        seq.add_child(if1)
        seq.add_child(assign3)

        return seq

    @staticmethod
    def prog_tree():
        """
        The prog program (from subject) implemented with our tree
        """
        tree_prog = Node("sequence")

        # Sequence 1 : if1
        if1 = Node("if")

        # condition if1
        compare1 = Node("compare", "<=")
        var1 = Node("variable", "x")
        cst1 = Node("constant", 0)
        compare1.add_child(var1)
        compare1.add_child(cst1)
        if1.add_child(compare1)

        # if body if1
        assign1 = Node("assign")
        var1 = Node("variable", "x")
        op1 = Node("operation", "-")
        cst2 = Node("constant", 0)
        var2 = Node("variable", "x")
        op1.add_child(cst2)
        op1.add_child(var2)
        assign1.add_child(var1)
        assign1.add_child(op1)
        if1.add_child(assign1)

        # else body if1
        assign2 = Node("assign")
        var3 = Node("variable", "x")
        op2 = Node("operation", "-")
        cst3 = Node("constant", 1)
        var4 = Node("variable", "x")
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
        var5 = Node("variable", "x")
        cst4 = Node("constant", 1)
        compare2.add_child(var5)
        compare2.add_child(cst4)
        if2.add_child(compare2)

        # if body if2
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        assign3.add_child(var6)
        assign3.add_child(cst5)
        if2.add_child(assign3)

        # else body if2
        assign4 = Node("assign")
        var7 = Node("variable", "x")
        op3 = Node("operation", "+")
        var8 = Node("variable", "x")
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
    def basic_if():
        """
        Creates a basic if node
        """
        if2 = Node("if")
        # condition if
        compare2 = Node("compare", "==")
        var5 = Node("variable", "x")
        cst4 = Node("constant", 1)
        compare2.add_child(var5)
        compare2.add_child(cst4)
        if2.add_child(compare2)
        # if body if
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        assign3.add_child(var6)
        assign3.add_child(cst5)
        if2.add_child(assign3)
        # else body if
        assign4 = Node("assign")
        var7 = Node("variable", "x")
        op3 = Node("operation", "+")
        var8 = Node("variable", "x")
        cst6 = Node("constant", 1)
        op3.add_child(var8)
        op3.add_child(cst6)
        assign4.add_child(var7)
        assign4.add_child(op3)
        if2.add_child(assign4)

        return if2

    @staticmethod
    def if_nested_seq():
        """
        Creates a if node in which the else part contains a sequence
        """
        if2 = Node("if")
        # condition if
        compare2 = Node("compare", "==")
        var5 = Node("variable", "x")
        cst4 = Node("constant", 1)
        compare2.add_child(var5)
        compare2.add_child(cst4)
        if2.add_child(compare2)
        # if body if
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        assign3.add_child(var6)
        assign3.add_child(cst5)
        if2.add_child(assign3)
        # else body if
        seq = Node("sequence")
        # 1 assign
        assign4 = Node("assign")
        var7 = Node("variable", "x")
        cst8 = Node("constant", 32)
        assign4.add_child(var7)
        assign4.add_child(cst8)
        seq.add_child(assign4)

        # 2 assign
        assign5 = Node("assign")
        var8 = Node("variable", "x")
        op = Node("operation", "*")
        var9 = Node("variable", "x")
        cst9 = Node("constant", 4)
        op.add_child(var9)
        op.add_child(cst9)
        assign5.add_child(var8)
        assign5.add_child(op)
        seq.add_child(assign5)

        if2.add_child(seq)
        return if2

    @staticmethod
    def basic_while_tree():
        """
        while X < 5
        X := X + 1
        """
        while_node = Node("while")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        while_node.add_child(comp)

        # action node
        assign = Node("assign")
        var1 = Node("variable", "x")
        op = Node("operation", "+")
        var2 = Node("variable", "x")
        cst = Node("constant", 1)
        op.add_child(var2)
        op.add_child(cst)
        assign.add_child(var1)
        assign.add_child(op)
        while_node.add_child(assign)
        return while_node

    @staticmethod
    def while_tree_with_seq():
        while_node = Node("while")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        while_node.add_child(comp)

        # action node
        seq = Node("sequence")
        assign1 = Node("assign")
        var1 = Node("variable", "x")
        op1 = Node("operation", "+")
        var2 = Node("variable", "x")
        var3 = Node("variable", "x")
        op1.add_child(var2)
        op1.add_child(var3)
        assign1.add_child(var1)
        assign1.add_child(op1)

        assign2 = Node("assign")
        var4 = Node("variable", "x")
        op2 = Node("operation", "-")
        var6 = Node("variable", "x")
        cst = Node("constant", 1)
        op2.add_child(var6)
        op2.add_child(cst)
        assign2.add_child(var4)
        assign2.add_child(op2)

        seq.add_child(assign1)
        seq.add_child(assign2)

        while_node.add_child(seq)
        return while_node

    @staticmethod
    def seq_with_while():
        seq = Node("sequence")
        if_part = GeneratorAstTree.basic_if()
        while_part = GeneratorAstTree.basic_while_tree()
        seq.add_child(if_part)
        seq.add_child(while_part)
        return seq

    @staticmethod
    def while_with_if():
        while_node = Node("while")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        while_node.add_child(comp)
        # action node
        if_node = GeneratorAstTree.basic_if()
        while_node.add_child(if_node)
        return while_node

    @staticmethod
    def if_with_while():
        if_node = Node("if")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        if_node.add_child(comp)

        # if body
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        assign3.add_child(var6)
        assign3.add_child(cst5)
        if_node.add_child(assign3)

        # else body - with while
        while_part = GeneratorAstTree.basic_while_tree()
        if_node.add_child(while_part)
        return if_node

    @staticmethod
    def if_with_if():
        if_main_node = Node("if")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        if_main_node.add_child(comp)
        # if body
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        assign3.add_child(var6)
        assign3.add_child(cst5)
        if_main_node.add_child(assign3)
        # else body - if nested
        nested_if = GeneratorAstTree.basic_if()
        if_main_node.add_child(nested_if)
        return if_main_node
