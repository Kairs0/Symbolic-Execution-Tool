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
- implement criteria tests (4/9) on coverage analysis
- push much further on ast to cfg converter

- explain CFG modelling and its consequences on the way tests are made

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