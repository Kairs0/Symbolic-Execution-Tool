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


## WIP - todos
- manage and, or in comparisons in cfg construction
- implement criteria tests (3/9) on coverage analysis
- push tests much further on ast to cfg converter

- parsing : see https://tomassetti.me/parsing-in-python/#tools
- also see https://github.com/c2nes/javalang.git
- and also: http://lisperator.net/pltut/parser/

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
    
## Structures - descriptions

#### Control Flow Graph - CFG

The CFG Graph is managed as a python dictionary.
- The key is the number of the node
- The value is a list containing information about the node:

    - Value[0] contains the command type: it can be "assign", "while", "if" or "skip"
    
   
*"if" and "while" commands:*
- Value[1] is the comparator. It can be "<=", ..., ">="
- Value[2] is a length 2 list of values on which the Value[1] operates.
    - list[0] is the first value to be compared,
    - list[1] the second value.

These two values can either be a string ("x" or "y") or an int

- Value[3] contains a list of 2 integer. The first one is the following node when the statement is true, the second one the following node when the statement is false.

*"assign" commands:*
- Value[1] is a dic {variable: new value}, (keys and values are string, eg {'x': '4'}
- Value[2] is the number of the following node (list)

*For "skip" commands:*
- Value[1] is the number of the following node (list)

Value zero represents the _ sign (absence of following node).

###### An example: graph for "prog" program
```
graph_prog = {
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
        }
```