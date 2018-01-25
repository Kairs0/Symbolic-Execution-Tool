import unittest

from ast_to_cfg import AstToCfgConverter, check_children_are_cst_or_var
from ast_tree import GeneratorAstTree


class TestAstToCfgMethods(unittest.TestCase):
    def test_childrenAreCstOrVar(self):
        if_tree = GeneratorAstTree.create_if_cfg()
        body_part = if_tree.children[1]
        self.assertEqual(check_children_are_cst_or_var(if_tree), False)
        self.assertEqual(check_children_are_cst_or_var(body_part), True)

    def test_treat_seq_node(self):
        prog_tree = GeneratorAstTree.create_prog_tree()
        parser = AstToCfgConverter(prog_tree)
        result = parser.treat_seq_node(prog_tree)
        expected = {
            1: ('if', '<=', ["x", 0], (2, 3)),
            2: ('assign', '0-x', '', 4),
            3: ('assign', '1-x', '', 4),
            4: ('if', '==', ["x", 1], (5, 6)),
            5: ('assign', '1', '', 7), 
            6: ('assign', 'x+1', '', 7)
        }
        self.assertEqual(result, expected)

    def test_treat_if_node(self):
        basic_if_tree = GeneratorAstTree.create_if_cfg()
        if_tree_with_seq = GeneratorAstTree.create_if_cfg_else_is_seq()
        parser = AstToCfgConverter(if_tree_with_seq)
        result = parser.treat_if_node(if_tree_with_seq)

        parser_for_basic = AstToCfgConverter(basic_if_tree)
        result_for_basic = parser_for_basic.treat_if_node(basic_if_tree)

        expected = {
            1: ('if', '==', ["x", 1], (2, 3)),
            2: ('assign', '1', '', 5),
            3: ('assign', '32', '', 4),
            4: ('assign', 'x*4', '', 5)
        }

        expected_basic = {
            1: ('if', '==', ["x", 1], (2, 3)),
            2: ('assign', '1', '', 4),
            3: ('assign', 'x+1', '', 4)
        }

        self.assertEqual(result, expected)
        self.assertEqual(result_for_basic, expected_basic)

    def test_get_height(self):
        prog_tree = GeneratorAstTree.create_prog_tree()
        basic_if_tree = GeneratorAstTree.create_if_cfg()
        h_prog = prog_tree.get_height()
        h_if = basic_if_tree.get_height()
        self.assertEqual(h_prog, 4)
        self.assertEqual(h_if, 3)

    def test_treat_compare_node(self):
        pass


if __name__ == "__main__":
    unittest.main()
