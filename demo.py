from analysis_coverage import *
from generator import *
import time


def main():
    # DEMO ON PROG 1

    test_values = read_test_file("sets_tests_txt/test.txt")
    ast_tree_prog = GeneratorAstTree.get_ast_from_name("prog_1")
    # Convert AST to CFG
    converter = AstToCfgConverter(ast_tree_prog)
    cfg_graph_prog = converter.get_cfg_graph()
    # Process tests to get coverage
    print("Coverage analysis on prog offered in subject and set of value for x: -3;-2;-1;0;1;2;3")
    calc_coverage(cfg_graph_prog, test_values, True)
    # Generate tests to match coverage
    print("Generation tests for program prog ...")
    start = time.time()
    generate_sets_tests(cfg_graph_prog, 'generated_tests', 'generated_prog.txt')
    print("End generation test values (" + str(round(time.time() - start, 2)) + "s)")

    # DEMO ON FACT PROG

    print("\n\n")
    test_values = read_test_file("sets_tests_txt/test.txt")
    ast_tree_fact = GeneratorAstTree.get_ast_from_name("fact")
    # Convert AST to CFG
    converter = AstToCfgConverter(ast_tree_fact)
    cfg_graph_fact = converter.get_cfg_graph()
    # Process tests to get coverage
    print("Coverage analysis on factorial program (see code in sources_txt/fact.txt) for x: -3;-2;-1;0;1;2;3")
    calc_coverage(cfg_graph_fact, test_values, True)
    print("Generation test for factorial program")
    start = time.time()
    generate_sets_tests(cfg_graph_fact, 'generated_tests', 'generated_fact.txt')
    print("End generation test values (" + str(round(time.time() - start, 2)) + "s)")


if __name__ == '__main__':
    main()
