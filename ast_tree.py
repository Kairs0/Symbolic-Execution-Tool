#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#### AST Tree structure:

# Each node has a category (string), values can be : 
sequence, if, variable, constant, operation, assign, compare, while, logic

# Each node has a list of nodes which are his children

# A node can have a data (for constant, operation, compare, variable)
constant: data is the value of the constant,
variable: data is the name of the variable
compare : data is the operator (==, <=, ...)
operation: data is the operator (+, *, ...)
logic: data is the logic addition (and, or)

"""


class Node(object):
    def __init__(self, category, data=None):
        self.data = data
        self.category = category
        self.children = []
        self.level = 0

    def add_child(self, obj):
        self.children.append(obj)

    def add_children(self, children):
        self.children.extend(children)

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
    def get_ast_from_name(name):
        if name == "prog_1":
            return GeneratorAstTree.prog_tree()

    @staticmethod
    def clean_cnf_conditions():
        or_1 = GeneratorAstTree.or_condition()
        or_2 = GeneratorAstTree.or_condition()
        and_node = Node("logic", "and")
        and_node.add_children([or_1, or_2])
        return and_node

    @staticmethod
    def or_condition():
        # condition
        # condition 1
        compare1 = Node("compare", "<=")
        var1 = Node("variable", "x")
        cst1 = Node("constant", 0)
        compare1.add_child(var1)
        compare1.add_child(cst1)
        # condition 2
        compare2 = Node("compare", ">")
        var2 = Node("variable", "y")
        cst2 = Node("constant", 2)
        compare2.add_child(var2)
        compare2.add_child(cst2)
        # and logic
        or_node = Node("logic", "or")
        or_node.add_child(compare1)
        or_node.add_child(compare2)
        return or_node

    @staticmethod
    def and_condition():
        # condition
        # condition 1
        compare1 = Node("compare", "<=")
        var1 = Node("variable", "x")
        cst1 = Node("constant", 0)
        compare1.add_child(var1)
        compare1.add_child(cst1)
        # condition 2
        compare2 = Node("compare", ">")
        var2 = Node("variable", "y")
        cst2 = Node("constant", 2)
        compare2.add_child(var2)
        compare2.add_child(cst2)
        # and logic
        and_node = Node("logic", "and")
        and_node.add_child(compare1)
        and_node.add_child(compare2)

        return and_node

    @staticmethod
    def if_with_and_condition():
        """
        if (X <= 0 and Y > 2)
        then X:= Y
        else Y:=X
        :returns: ast tree
        """
        if_node = Node("if")

        # condition
        # condition 1
        compare1 = Node("compare", "<=")
        var1 = Node("variable", "x")
        cst1 = Node("constant", 0)
        compare1.add_child(var1)
        compare1.add_child(cst1)
        # condition 2
        compare2 = Node("compare", ">")
        var2 = Node("variable", "y")
        cst2 = Node("constant", 2)
        compare2.add_child(var2)
        compare2.add_child(cst2)
        # and logic
        and_node = Node("logic", "and")
        and_node.add_child(compare1)
        and_node.add_child(compare2)

        # then body
        assign = Node("assign")
        var2 = Node("variable", "x")
        var3 = Node("variable", "y")
        assign.add_child(var2)
        assign.add_child(var3)

        # else body
        assign2 = Node("assign")
        var4 = Node("variable", "y")
        var5 = Node("variable", "x")
        assign2.add_child(var4)
        assign2.add_child(var5)

        # setting if node
        if_node.add_children([and_node, assign, assign2])
        return if_node

    @staticmethod
    def seq_if_and_assign():
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
    def complex_sequence():
        seq = Node("sequence")
        part1 = GeneratorAstTree.if_nested_seq()
        part2 = GeneratorAstTree.if_with_two_while()
        part3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        part3.add_child(var6)
        part3.add_child(cst5)
        seq.add_child(part1)
        seq.add_child(part2)
        seq.add_child(part3)
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
    def if_with_while_right_part():
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
    def if_with_while_left_part():
        if_node = Node("if")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        if_node.add_child(comp)

        # if body - with while
        while_part = GeneratorAstTree.basic_while_tree()
        if_node.add_child(while_part)

        # else body - without while
        assign3 = Node("assign")
        var6 = Node("variable", "x")
        cst5 = Node("constant", 1)
        assign3.add_child(var6)
        assign3.add_child(cst5)
        if_node.add_child(assign3)
        return if_node

    @staticmethod
    def if_with_two_while():
        if_node = Node("if")
        # condition node
        comp = Node("compare", "<")
        var0 = Node("variable", "x")
        var5 = Node("constant", 5)
        comp.add_child(var0)
        comp.add_child(var5)
        if_node.add_child(comp)

        # if body - with while
        while_part = GeneratorAstTree.basic_while_tree()
        if_node.add_child(while_part)

        # else body - also with while
        while_part_else = GeneratorAstTree.basic_while_tree()
        if_node.add_child(while_part_else)
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

    @staticmethod
    def fact_tree():
        seq = Node("sequence")

        # seq part 1
        assign1 = Node("assign")
        var1 = Node("variable", "n")
        cst = Node("constant", 1)
        assign1.add_child(var1)
        assign1.add_child(cst)

        # seq part 2
        whileloop = Node("while")

        # compar
        comp = Node("compare", ">=")
        var2 = Node("variable", "x")
        cst1 = Node("constant", 1)
        comp.add_child(var2)
        comp.add_child(cst1)

        # body while
        seq_inside_while = Node("sequence")

        assign2 = Node("assign")
        var3 = Node("variable", "n")
        op1 = Node("operation", "*")
        var4 = Node("variable", "n")
        var5 = Node("variable", "x")
        op1.add_child(var4)
        op1.add_child(var5)
        assign2.add_child(var3)
        assign2.add_child(op1)

        assign3 = Node("assign")
        var4 = Node("variable", "x")
        op2 = Node("operation", "-")
        var5 = Node("variable", "x")
        cst2 = Node("constant", 1)
        op2.add_child(var5)
        op2.add_child(cst2)
        assign3.add_child(var4)
        assign3.add_child(op2)

        seq_inside_while.add_child(assign2)
        seq_inside_while.add_child(assign3)

        whileloop.add_child(comp)
        whileloop.add_child(seq_inside_while)

        seq.add_child(assign1)
        seq.add_child(whileloop)
        return seq

    @staticmethod
    def false_fact_tree():
        seq = Node("sequence")
        part1 = Node("while")

        # condition while
        comp = Node("compare", "!=")
        var0 = Node("variable", "i")
        op1 = Node("operation", "+")
        var1 = Node("variable", "x")
        cst1 = Node("constant", 1)
        op1.add_child(var1)
        op1.add_child(cst1)
        comp.add_child(var0)
        comp.add_child(op1)

        # body while
        seq_while = Node("sequence")
        ass1 = Node("assign")
        var2 = Node("variable", "i")
        op2 = Node("operation", "+")
        var3 = Node("variable", "i")
        cst2 = Node("constant", 1)
        op2.add_child(var3)
        op2.add_child(cst2)
        ass1.add_child(var2)
        ass1.add_child(op2)

        ass2 = Node("assign")
        var3 = Node("variable", "f")
        op3 = Node("operation", "*")
        var4 = Node("variable", "f")
        var5 = Node("variable", "i")
        op3.add_child(var4)
        op3.add_child(var5)
        ass2.add_child(var3)
        ass2.add_child(op3)

        seq_while.add_child(ass1)
        seq_while.add_child(ass2)

        part1.add_child(comp)
        part1.add_child(seq_while)

        part2 = Node("assign")
        var6 = Node("variable", "i")
        cst3 = Node("constant", 1)
        part2.add_child(var6)
        part2.add_child(cst3)

        seq.add_child(part1)
        seq.add_child(part2)
        return seq
