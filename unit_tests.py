#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from ast_to_cfg import AstToCfgConverter
from ast_tree import GeneratorAstTree
from process_cfg_tools import *


class TestAstToCfgMethods(unittest.TestCase):
    def test_childrenAreCstOrVar(self):
        if_tree = GeneratorAstTree.basic_if()
        body_part = if_tree.children[1]
        self.assertEqual(AstToCfgConverter.check_children_are_cst_or_var(if_tree), False)
        self.assertEqual(AstToCfgConverter.check_children_are_cst_or_var(body_part), True)

    def test_treat_multiple_cond(self):
        and_cond = GeneratorAstTree.and_condition()
        or_cond = GeneratorAstTree.or_condition()
        complex_cond = GeneratorAstTree.clean_cnf_conditions()
        converter = AstToCfgConverter(and_cond)
        # or_cond
        result = converter.treat_composed_boolean_expr(or_cond)
        expected = [[('<=', ['x', 0]), ('>', ['y', 2])]]
        self.assertEqual(result, expected)
        # and_cond
        result = converter.treat_composed_boolean_expr(and_cond)
        expected = [[('<=', ['x', 0])], [('>', ['y', 2])]]
        self.assertEqual(result, expected)
        # complex cond (cnf format)
        result = converter.treat_composed_boolean_expr(complex_cond)
        expected = [[('<=', ['x', 0]), ('>', ['y', 2])], [('<=', ['x', 0]), ('>', ['y', 2])]]
        self.assertEqual(result, expected)

    def test_treat_while_node(self):
        # test simple while loop
        while_tree = GeneratorAstTree.basic_while_tree()
        parser = AstToCfgConverter(while_tree)
        result = parser.treat_while_node(while_tree)
        expected = {
            1: ['while', [[('<', ['x', 5])]], [2, 3]],
            2: ['assign', {'x': 'x+1'}, [1]],
        }
        self.assertEqual(result, expected)

        # test tree with sequence inside
        while_tree_seq = GeneratorAstTree.while_tree_with_seq()
        parser2 = AstToCfgConverter(while_tree_seq)
        result2 = parser2.treat_while_node(while_tree_seq)

        expected2 = {
            1: ["while", [[('<', ['x', 5])]], [2, 4]],
            2: ['assign', {'x': 'x+x'}, [3]],
            3: ['assign', {'x': 'x-1'}, [1]]
        }

        self.assertEqual(result2, expected2)

        # test while with if inside
        while_with_if = GeneratorAstTree.while_with_if()
        parser3 = AstToCfgConverter(while_with_if)
        result3 = parser3.treat_while_node(while_with_if)

        expected3 = {
            1: ['while', [[('<', ['x', 5])]], [2, 5]],
            2: ['if', [[('==', ["x", 1])]], [3, 4]],
            3: ['assign', {'x': '1'}, [1]],
            4: ['assign', {'x': 'x+1'}, [1]]
        }

        self.assertEqual(result3, expected3)

        # TODO: test with more complex if loop (sequence inside right left, ...)

    def test_treat_seq_node(self):
        prog_tree = GeneratorAstTree.prog_tree()
        parser = AstToCfgConverter(prog_tree)
        result = parser.treat_seq_node(prog_tree)
        expected = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [7]],
            6: ['assign', {'x': 'x+1'}, [7]]
        }
        self.assertEqual(result, expected)

    def test_treat_seq_with_while(self):
        seq_tree = GeneratorAstTree.seq_with_while()

        expected = {
            1: ['if', [[('==', ["x", 1])]], [2, 3]],
            2: ['assign', {'x': '1'}, [4]],
            3: ['assign', {'x': 'x+1'}, [4]],
            4: ['while', [[('<', ['x', 5])]], [5, 6]],
            5: ['assign', {'x': 'x+1'}, [4]]
        }
        parser = AstToCfgConverter(seq_tree)
        result = parser.treat_seq_node(seq_tree)

        self.assertEqual(result, expected)

    def test_treat_if_node(self):
        # basic if tree
        basic_if_tree = GeneratorAstTree.basic_if()
        parser_for_basic = AstToCfgConverter(basic_if_tree)
        result_for_basic = parser_for_basic.treat_if_node(basic_if_tree)
        expected_basic = {
            1: ['if', [[('==', ["x", 1])]], [2, 3]],
            2: ['assign', {'x': '1'}, [4]],
            3: ['assign', {'x': 'x+1'}, [4]]
        }
        self.assertEqual(result_for_basic, expected_basic)

        # if with sequence inside
        if_tree_with_seq = GeneratorAstTree.if_nested_seq()
        parser = AstToCfgConverter(if_tree_with_seq)
        result = parser.treat_if_node(if_tree_with_seq)
        expected = {
            1: ['if', [[('==', ["x", 1])]], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['assign', {'x': '32'}, [4]],
            4: ['assign', {'x': 'x*4'}, [5]]
        }
        self.assertEqual(result, expected)

        # if with nested while (right)
        if_with_while_right = GeneratorAstTree.if_with_while_right_part()
        parser_for_if_while_right = AstToCfgConverter(if_with_while_right)
        result_for_if_while_right = parser_for_if_while_right.treat_if_node(if_with_while_right)

        expected_for_if_while = {
            1: ['if', [[('<', ['x', 5])]], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['while', [[('<', ['x', 5])]], [4, 5]],
            4: ['assign', {'x': 'x+1'}, [3]]
        }

        self.assertEqual(result_for_if_while_right, expected_for_if_while)

        # if with nested while (left)
        if_with_while_left = GeneratorAstTree.if_with_while_left_part()
        parser_for_if_while_left = AstToCfgConverter(if_with_while_left)
        result_for_if_while_left = parser_for_if_while_left.treat_if_node(if_with_while_left)

        expected_for_if_while_left = {
            1: ['if', [[('<', ['x', 5])]], [2, 4]],
            2: ['while', [[('<', ['x', 5])]], [3, 5]],
            3: ['assign', {'x': 'x+1'}, [2]],
            4: ['assign', {'x': '1'}, [5]]
        }
        self.assertEqual(result_for_if_while_left, expected_for_if_while_left)

        # if with two nested while (left and right)
        if_with_two_while = GeneratorAstTree.if_with_two_while()
        parser_for_if_two_while = AstToCfgConverter(if_with_two_while)
        result_for_if_two_while = parser_for_if_two_while.treat_if_node(if_with_two_while)

        expected_for_if_two_while = {
            1: ['if', [[('<', ['x', 5])]], [2, 4]],
            2: ['while', [[('<', ['x', 5])]], [3, 6]],
            3: ['assign', {'x': 'x+1'}, [2]],
            4: ['while', [[('<', ['x', 5])]], [5, 6]],
            5: ['assign', {'x': 'x+1'}, [4]],
        }

        self.assertEqual(result_for_if_two_while, expected_for_if_two_while)

        # if with nested if
        if_with_if = GeneratorAstTree.if_with_if()
        parser_for_if_if = AstToCfgConverter(if_with_if)
        result_for_if_if = parser_for_if_if.treat_if_node(if_with_if)
        expected_for_if_within_if = {
            1: ['if', [[('<', ['x', 5])]], [2, 3]],
            2: ['assign', {'x': '1'}, [6]],
            3: ['if', [[('==', ['x', 1])]], [4, 5]],
            4: ['assign', {'x': '1'}, [6]],
            5: ['assign', {'x': 'x+1'}, [6]]
        }
        self.assertEqual(result_for_if_if, expected_for_if_within_if)

    def test_get_height(self):
        prog_tree = GeneratorAstTree.prog_tree()
        basic_if_tree = GeneratorAstTree.basic_if()
        h_prog = prog_tree.get_height()
        h_if = basic_if_tree.get_height()
        self.assertEqual(h_prog, 4)
        self.assertEqual(h_if, 3)

    def test_get_cfg_graph(self):
        assign_tree = GeneratorAstTree.seq_if_and_assign()
        parser = AstToCfgConverter(assign_tree)
        result = parser.get_cfg_graph()
        expected = {
            1: ['if', [[('<=', ['x', 0])]], [2, 3]],
            2: ['assign', {'y': 'x'}, [4]],
            3: ['assign', {'y': '0-x'}, [4]],
            4: ['assign', {'x': 'y*2'}, [0]]
        }

        self.assertEqual(result, expected)

        prog_tree = GeneratorAstTree.prog_tree()
        parser_prog = AstToCfgConverter(prog_tree)
        result_prog = parser_prog.get_cfg_graph()
        expected_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }

        self.assertEqual(result_prog, expected_prog)

        complex_tree = GeneratorAstTree.complex_sequence()
        parser_complex = AstToCfgConverter(complex_tree)
        result_complex = parser_complex.get_cfg_graph()
        expected_complex = {
            1: ['if', [[('==', ["x", 1])]], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['assign', {'x': '32'}, [4]],
            4: ['assign', {'x': 'x*4'}, [5]],
            5: ['if', [[('<', ['x', 5])]], [6, 8]],
            6: ['while', [[('<', ['x', 5])]], [7, 10]],
            7: ['assign', {'x': 'x+1'}, [6]],
            8: ['while', [[('<', ['x', 5])]], [9, 10]],
            9: ['assign', {'x': 'x+1'}, [8]],
            10: ['assign', {'x': '1'}, [0]]
        }

        self.assertEqual(result_complex, expected_complex)

        fact_tree = GeneratorAstTree.fact_tree()
        parser_fact = AstToCfgConverter(fact_tree)
        result_fact = parser_fact.get_cfg_graph()

        expected_fact = {
            1: ['assign', {'n': '1'}, [2]],
            2: ['while', [[('>=', ['x', 1])]], [3, 0]],
            3: ['assign', {'n': 'n*x'}, [4]],
            4: ['assign', {'x': 'x-1'}, [2]]
        }

        self.assertEqual(result_fact, expected_fact)


class TestProcessCfgMethods(unittest.TestCase):
    def test_get_children(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }

        result = get_children(2, graph_prog)

        expected = {0, 4, 5, 6}
        self.assertEqual(result, expected)
        result = get_children(1, graph_prog)
        expected = {0, 2, 3, 4, 5, 6}
        self.assertEqual(result, expected)

        other_graph = {
            1: ['if', [[('==', ["x", 1])]], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['assign', {'x': '32'}, [4]],
            4: ['assign', {'x': 'x*4'}, [5]],
            5: ['if', [[('<', ['x', 5])]], [6, 8]],
            6: ['while', [[('<', ['x', 5])]], [7, 10]],
            7: ['assign', {'x': 'x+1'}, [6]],
            8: ['while', [[('<', ['x', 5])]], [9, 10]],
            9: ['assign', {'x': 'x+1'}, [8]],
            10: ['assign', {'x': '1'}, [0]]
        }

        result = get_children(6, other_graph)
        expected = {0, 6, 7, 10}
        self.assertEqual(result, expected)

    def test_get_accessible_graph(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        result = get_accessible_graph(graph_prog, 2)
        expected = {
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        self.assertEqual(result, expected)

        result = get_accessible_graph(graph_prog, 1)
        expected = {
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        self.assertEqual(result, expected)

        other_graph = {
            1: ['if', [[('==', ["x", 1])]], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['assign', {'x': '32'}, [4]],
            4: ['assign', {'x': 'x*4'}, [5]],
            5: ['if', [[('<', ['x', 5])]], [6, 8]],
            6: ['while', [[('<', ['x', 5])]], [7, 10]],
            7: ['assign', {'x': 'x+1'}, [6]],
            8: ['while', [[('<', ['x', 5])]], [9, 10]],
            9: ['assign', {'x': 'x+1'}, [8]],
            10: ['assign', {'x': '1'}, [0]]
        }
        result = get_accessible_graph(other_graph, 6)
        expected = {
            6: ['while', [[('<', ['x', 5])]], [7, 10]],
            7: ['assign', {'x': 'x+1'}, [6]],
            10: ['assign', {'x': '1'}, [0]]
        }
        self.assertEqual(result, expected)

    def test_process_value_test(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        result_path, result_var = process_value_test(graph_prog, {'x': 3})
        self.assertEqual(result_var['x'], -1)
        result_path, result_var = process_value_test(graph_prog, {'x': -1})
        self.assertEqual(result_var['x'], 1)

        graph_while = {
            1: ["while", [[('<', ['x', 5])]], [2, 4]],
            2: ['assign', {'x': 'x+x'}, [3]],
            3: ['assign', {'x': 'x-1'}, [1]],
            4: ['assign', {'y': 'x*2'}, [0]]
        }

        result_path, result_var = process_value_test(graph_while, {'x': 2, 'y': 0})
        self.assertEqual(result_var['y'], 10)
        self.assertEqual(result_var['x'], 5)

        graph_fact = {
            1: ['assign', {'n': '1'}, [2]],
            2: ['while', [[('>=', ['x', 1])]], [3, 0]],
            3: ['assign', {'n': 'n*x'}, [4]],
            4: ['assign', {'x': 'x-1'}, [2]]
        }

        result_path, result_var = process_value_test(graph_fact, {'x': 5, 'n': 1})

        self.assertEqual(result_var['n'], 120)
        self.assertEqual(result_var['x'], 0)
        expected_path = [1, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 0]
        self.assertEqual(result_path, expected_path)

    def test_get_all_paths(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        expected = [[1, 2, 4, 5, 0], [1, 2, 4, 6, 0], [1, 3, 4, 5, 0], [1, 3, 4, 6, 0]]

        all_paths = get_all_paths(graph_prog, 1)

        self.assertEqual(all_paths, expected)

    def test_get_father_for_node(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        fathers = get_father_for_node(1, graph_prog)
        expected = []
        self.assertEqual(fathers, expected)
        fathers = get_father_for_node(4, graph_prog)
        expected = [2, 3]
        self.assertEqual(fathers, expected)
        fathers = get_father_for_node(0, graph_prog)
        expected = [5, 6]
        self.assertEqual(fathers, expected)
        fathers = get_father_for_node(5, graph_prog)
        expected = [4]
        self.assertEqual(fathers, expected)

    def test_path_to_node(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        result = path_to_node(6, graph_prog)
        expected = [6, 4, 2, 1]
        self.assertEqual(result, expected)

        result = path_to_node(3, graph_prog)
        expected = [3, 1]
        self.assertEqual(result, expected)

        graph_fact = {
            1: ['assign', {'n': '1'}, [2]],
            2: ['while', [[('>=', ['x', 1])]], [3, 0]],
            3: ['assign', {'n': 'n*x'}, [4]],
            4: ['assign', {'x': 'x-1'}, [2]]
        }
        result = path_to_node(4, graph_fact)
        expected = [4, 3, 2, 1]
        self.assertEqual(result, expected)

    def test_detailed_steps_path(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        result = detailed_steps_path(path_to_node(3, graph_prog), graph_prog)
        expected = {
            1: [[[('<=', ["x", 0])]], False],
            3: {'x': '1-x'}
        }
        self.assertEqual(result, expected)

        result = detailed_steps_path(path_to_node(5, graph_prog), graph_prog)
        expected = {
            1: [[[('<=', ["x", 0])]], True],
            2: {'x': '0-x'},
            4: [[[('==', ["x", 1])]], True],
            5: {'x': '1'}
        }
        self.assertEqual(result, expected)

        graph_fact = {
            1: ['assign', {'n': '1'}, [2]],
            2: ['while', [[('>=', ['x', 1])]], [3, 0]],
            3: ['assign', {'n': 'n*x'}, [4]],
            4: ['assign', {'x': 'x-1'}, [2]]
        }
        result = detailed_steps_path(path_to_node(3, graph_fact), graph_fact)
        expected = {
            1: {'n': '1'},
            2: [[[('>=', ['x', 1])]], True],
            3: {'n': 'n*x'}
        }
        self.assertEqual(result, expected)

    def test_transform_bool_expr_to_str(self):
        result = transform_bool_expr_to_str([[('<=', ['x', 0]), ('>', ['y', 2])], [('<=', ['x', 0]), ('>', ['y', 2])]])
        expected = '(x<=0 or y>2) and (x<=0 or y>2)'
        self.assertEqual(result, expected)

    def test_path_predicate(self):
        graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }

        to_node_five = path_to_node(5, graph_prog)
        detailed_path = detailed_steps_path(to_node_five, graph_prog)

        # print(detailed_path)

        result = path_predicate(detailed_path, graph_prog)
        expected = ['(x1<=0)', 'x2=0-x1', '(x4==1)']
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
