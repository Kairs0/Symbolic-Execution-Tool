import unittest
from astToCfg import astToCfg, childrenAreCstOrVar
from asttree import Node, GeneratorAstTree

class TestAstToCfgMethods(unittest.TestCase):
    def test_childrenAreCstOrVar(self):
        ifTree = GeneratorAstTree.create_if_cfg()
        bodyPart = ifTree.children[1]
        self.assertEqual(childrenAreCstOrVar(ifTree), False)
        self.assertEqual(childrenAreCstOrVar(bodyPart), True)

    def test_treat_seq_node(self):
        prog_tree = GeneratorAstTree.create_prog_tree()
        parser = astToCfg(prog_tree)
        result = parser.treat_seq_node(prog_tree)
        expected = {
            1: ('if', '<=', [0], (2, 3)),
            2: ('assign', '0-X', '', 4),
            3: ('assign', '1-X', '', 4),
            4: ('if', '==', [1], (5, 6)),
            5: ('assign', '1', '', 7), 
            6: ('assign', 'X+1', '', 7)
        }
        self.assertEqual(result, expected)

    def test_treat_if_node(self):
        basic_if_tree = GeneratorAstTree.create_if_cfg()
        if_tree_with_seq = GeneratorAstTree.create_if_cfg_else_is_seq()
        parser = astToCfg(if_tree_with_seq)
        result = parser.treat_if_node(if_tree_with_seq)

        parserBasic = astToCfg(basic_if_tree)
        resultBasic = parserBasic.treat_if_node(basic_if_tree)

        expected = {
            1: ('if', '==', [1], (2, 3)), 
            2: ('assign', '1', '', 5), 
            3: ('assign', '32', '', 4), 
            4: ('assign', 'X*4', '', 5)
        }

        expectedBasic = {
            1: ('if', '==', [1], (2, 3)),
            2: ('assign', '1', '', 4),
            3: ('assign', 'X+1', '', 4)
        }

        self.assertEqual(result, expected)
        self.assertEqual(resultBasic, expectedBasic)

    def test_treat_compare_node(self):
        pass



if __name__ == "__main__":
    unittest.main()

    # parser = astToCfg(ifTree)

    # print(parser.treat_compare_node(ifTree.children[0]))

    # print(parser.treat_operation_node(elsePart.children[1]))

    # print(parser.treat_assign_node(elsePart))

    # print(parser.treat_if_node(ifTree))

    # recent

    # prog_tree = GeneratorAstTree.create_prog_tree()

    # parser2 = astToCfg(prog_tree)

    # print(parser2.treat_seq_node(prog_tree))

    # a = GeneratorAstTree.create_if_cfg_else_is_seq()

    # parser3 = astToCfg(a)

    # print(parser3.treat_if_node(a))

