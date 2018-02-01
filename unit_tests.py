import unittest

from ast_to_cfg import AstToCfgConverter
from ast_tree import GeneratorAstTree
from process_tests import process_value_test


class TestAstToCfgMethods(unittest.TestCase):
    def test_childrenAreCstOrVar(self):
        if_tree = GeneratorAstTree.basic_if()
        body_part = if_tree.children[1]
        self.assertEqual(AstToCfgConverter.check_children_are_cst_or_var(if_tree), False)
        self.assertEqual(AstToCfgConverter.check_children_are_cst_or_var(body_part), True)

    def test_treat_while_node(self):
        # test simple while loop
        while_tree = GeneratorAstTree.basic_while_tree()
        parser = AstToCfgConverter(while_tree)
        result = parser.treat_while_node(while_tree)
        expected = {
            1: ['while', '<', ['x', 5], [2, 3]],
            2: ['assign', {'x': 'x+1'}, [1]],
        }
        self.assertEqual(result, expected)

        # test tree with sequence inside
        while_tree_seq = GeneratorAstTree.while_tree_with_seq()
        parser2 = AstToCfgConverter(while_tree_seq)
        result2 = parser2.treat_while_node(while_tree_seq)

        expected2 = {
            1: ["while", '<', ['x', 5], [2, 4]],
            2: ['assign', {'x': 'x+x'}, [3]],
            3: ['assign', {'x': 'x-1'}, [1]]
        }

        self.assertEqual(result2, expected2)

        # test while with if inside
        while_with_if = GeneratorAstTree.while_with_if()
        parser3 = AstToCfgConverter(while_with_if)
        result3 = parser3.treat_while_node(while_with_if)

        expected3 = {
            1: ['while', '<', ['x', 5], [2, 5]],
            2: ['if', '==', ["x", 1], [3, 4]],
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
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, [7]],
            6: ['assign', {'x': 'x+1'}, [7]]
        }
        self.assertEqual(result, expected)

    def test_treat_seq_with_while(self):
        seq_tree = GeneratorAstTree.seq_with_while()

        expected = {
            1: ['if', '==', ["x", 1], [2, 3]],
            2: ['assign', {'x': '1'}, [4]],
            3: ['assign', {'x': 'x+1'}, [4]],
            4: ['while', '<', ['x', 5], [5, 6]],
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
            1: ['if', '==', ["x", 1], [2, 3]],
            2: ['assign', {'x': '1'}, [4]],
            3: ['assign', {'x': 'x+1'}, [4]]
        }
        self.assertEqual(result_for_basic, expected_basic)

        # if with sequence inside
        if_tree_with_seq = GeneratorAstTree.if_nested_seq()
        parser = AstToCfgConverter(if_tree_with_seq)
        result = parser.treat_if_node(if_tree_with_seq)
        expected = {
            1: ['if', '==', ["x", 1], [2, 3]],
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
            1: ['if', '<', ['x', 5], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['while', '<', ['x', 5], [4, 5]],
            4: ['assign', {'x': 'x+1'}, [3]]
        }

        self.assertEqual(result_for_if_while_right, expected_for_if_while)

        # if with nested while (left)
        if_with_while_left = GeneratorAstTree.if_with_while_left_part()
        parser_for_if_while_left = AstToCfgConverter(if_with_while_left)
        result_for_if_while_left = parser_for_if_while_left.treat_if_node(if_with_while_left)

        expected_for_if_while_left = {
            1: ['if', '<', ['x', 5], [2, 4]],
            2: ['while', '<', ['x', 5], [3, 5]],
            3: ['assign', {'x': 'x+1'}, [2]],
            4: ['assign', {'x': '1'}, [5]]
        }
        self.assertEqual(result_for_if_while_left, expected_for_if_while_left)

        # if with two nested while (left and right)
        if_with_two_while = GeneratorAstTree.if_with_two_while()
        parser_for_if_two_while = AstToCfgConverter(if_with_two_while)
        result_for_if_two_while = parser_for_if_two_while.treat_if_node(if_with_two_while)

        expected_for_if_two_while = {
            1: ['if', '<', ['x', 5], [2, 4]],
            2: ['while', '<', ['x', 5], [3, 6]],
            3: ['assign', {'x': 'x+1'}, [2]],
            4: ['while', '<', ['x', 5], [5, 6]],
            5: ['assign', {'x': 'x+1'}, [4]],
        }

        self.assertEqual(result_for_if_two_while, expected_for_if_two_while)

        # if with nested if
        if_with_if = GeneratorAstTree.if_with_if()
        parser_for_if_if = AstToCfgConverter(if_with_if)
        result_for_if_if = parser_for_if_if.treat_if_node(if_with_if)
        expected_for_if_within_if = {
            1: ['if', '<', ['x', 5], [2, 3]],
            2: ['assign', {'x': '1'}, [6]],
            3: ['if', '==', ['x', 1], [4, 5]],
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
            1: ['if', '<=', ['x', 0], [2, 3]],
            2: ['assign', {'y': 'x'}, [4]],
            3: ['assign', {'y': '0-x'}, [4]],
            4: ['assign', {'x': 'y*2'}, [0]]
        }

        self.assertEqual(result, expected)

        prog_tree = GeneratorAstTree.prog_tree()
        parser_prog = AstToCfgConverter(prog_tree)
        result_prog = parser_prog.get_cfg_graph()
        expected_prog = {
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }

        self.assertEqual(result_prog, expected_prog)

        complex_tree = GeneratorAstTree.complex_sequence()
        parser_complex = AstToCfgConverter(complex_tree)
        result_complex = parser_complex.get_cfg_graph()
        expected_complex = {
            1: ['if', '==', ["x", 1], [2, 3]],
            2: ['assign', {'x': '1'}, [5]],
            3: ['assign', {'x': '32'}, [4]],
            4: ['assign', {'x': 'x*4'}, [5]],
            5: ['if', '<', ['x', 5], [6, 8]],
            6: ['while', '<', ['x', 5], [7, 10]],
            7: ['assign', {'x': 'x+1'}, [6]],
            8: ['while', '<', ['x', 5], [9, 10]],
            9: ['assign', {'x': 'x+1'}, [8]],
            10: ['assign', {'x': '1'}, [0]]
        }

        self.assertEqual(result_complex, expected_complex)


class TestProcessTestsMethods(unittest.TestCase):
    def test_process_value_test(self):
        graph_prog = {
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
        result_path, result_var = process_value_test(graph_prog, {'x': 3})
        self.assertEqual(result_var['x'], -1)
        result_path, result_var = process_value_test(graph_prog, {'x': -1})
        self.assertEqual(result_var['x'], 1)

        graph_while = {
            1: ["while", '<', ['x', 5], [2, 4]],
            2: ['assign', {'x': 'x+x'}, [3]],
            3: ['assign', {'x': 'x-1'}, [1]],
            4: ['assign', {'y': 'x*2'}, [0]]
        }
        result_path, result_var = process_value_test(graph_while, {'x': 2, 'y': 0})
        self.assertEqual(result_var['y'], 10)
        self.assertEqual(result_var['x'], 5)


if __name__ == "__main__":
    unittest.main()
