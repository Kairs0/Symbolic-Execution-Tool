# Formal Verification Project - 2018

A parser, test coverage checker and test generator for programs written in While language. 

The While language - grammar:

```
c ::= l : skip
| l : X := a
| (c; c)
| if l : b then c else c
| while l : b do c
```

## Content 

###### Files: 

- **my_parser.py**: module that contains a set of function to tokenize and parse a program written in While language to an Abstract Syntax Tree (AST).
- **ast_tree.py**: this module contains two class definitions : Node, which describes the structure of an AST 
 node, and GeneratorAstTree, used to write and directly programs in AST data structure.
- **ast_to_cfg.py**: a class that contains a set of function to transform an AST data structure into Control Flow Graph (CFG)
- **process_cfg_tools.py**: this module provides a set of functions that will be used to perform the analysis of test coverage.
- **analysis_coverage.py**: this modules contains a set of functions to perform structural analysis on program in AST.
- **symbolic_exec_tools.py**: this module provides a set of functions that will be used to perform test generation.
- **generator.py**: module used to generates sets of test according to tests criteria. 
- **unit_tests.py**: a few classes of test to perform tests on functions from different modules.

###### Directories:

- **sources_txt**: directory used to store files written in While language, on which we will perform test coverage analysis
- **sets_tests_txt**: directory used to store files containing sets of tests value
- **generated_tests**: directory where generated sets of tests value will be stored 


## Usage

- Test coverage
```
$ python analysis_coverage.py <source_file.txt> <set_tests.txt> [-v]
```
- Test generation
```
$ python generator.py <source_file.txt> 
```

## WIP - TODO
- test generation (2/8)
- refactor names
- comment and doc on most modules
- test coverage: provide a coverage (%) in each test
- report:
    - explain parsing, objective, and dealing with AST tree
    - explain CFG modelling and its consequences on the way tests are made
    - explain module ast to cfg
    - explain each coverage test
    - explain generation
    - results

    
## Structures - descriptions

#### Control Flow Graph - CFG

The CFG Graph is managed as a python dictionary.
- The key is the number of the node
- The value is a list containing information about the node:

    - Value[0] contains the command type: it can be "assign", "while", "if" or "skip"
    
   
*"if" and "while" commands:*
- Value[1] are the boolean expressions written in CNF format.

There is a AND relation between each element.

Each element is a list of tuples ; each tuple being a primitive condition (a < b)

There is a OR relation between each tuple. Each tuple is a description of the comparison to evaluate.
- tuple[0] is the operator. It can be "<=", ..., ">="
- tuple[1] is a length 2 list of values on which the tuple[0] operates.
    - list[0] is the first value to be compared,
    - list[1] the second value. These two values can either be a string ("x" or "y") or an int.

For instance, the statement 

```( x <= 0 ) and ( ( y == 3 ) or ( y < 0 ) )```
 
is stored as

```[[('<=',['x',0])],[('==', ['y', 3]),('<',['y, 0])]]```

- Value[2] contains a list of 2 integer. The first one is the following node when the statement is true, the second one the following node when the statement is false.

*"assign" commands:*
- Value[1] is a dic {variable: new value}, (keys and values are string, eg {'x': '4'}
- Value[2] is the number of the following node (list)

*For "skip" commands:*
- Value[1] is the number of the following node (list)

Value zero represents the _ sign (absence of following node).

###### An example: graph for "prog" program
```
graph_prog = {
            1: ['if', [[('<=', ["x", 0])]], [2, 3]],
            2: ['assign', {'x': '0-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', [[('==', ["x", 1])]], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
```

#### Abstract Syntax Tree - AST

The AST tree is a little hand-written tree. Each node has:
- A category :

```'sequence, if, variable, constant, operation, assign, compare, while, logic'```
- An optional data (depending on which category it belongs):
    - constant: data is the value of the constant,
    - variable: data is the name of the variable
    - compare : data is the operator (==, <=, ...)
    - operation: data is the operator (+, *, ...)
    - logic: data is the logic addition (and, or)
    
- A list of children, each of them being other node

## Summary parts of project
#### Part 1
- Inputs:
    - AST
    - Requirements
    - Value tests
- Output:
    - Coverage

#### Part 2
- Inputs:
    - AST
    - Requirements
- Output:
    - Values tests
    - Coverage
