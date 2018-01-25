import unittest
from astToCfg import astToCfg, childrenAreCstOrVar
from asttree import Node, GeneratorAstTree

class TestAstToCfgMethods(unittest.TestCase):
    def test_childrenAreCstOrVar(self):
        ifTree = GeneratorAstTree.create_if_cfg()
        bodyPart = ifTree.children[1]
        self.assertEqual(childrenAreCstOrVar(ifTree), False)
        self.assertEqual(childrenAreCstOrVar(bodyPart), True)

    def test_



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

