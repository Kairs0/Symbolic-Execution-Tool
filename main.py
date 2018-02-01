from ast_tree import GeneratorAstTree
from ast_to_cfg import AstToCfgConverter

if __name__ == "__main__":
    fact_tree = GeneratorAstTree.fact_tree()
    parser = AstToCfgConverter(fact_tree)
    graph_fact = parser.get_cfg_graph()

    print(graph_fact)
