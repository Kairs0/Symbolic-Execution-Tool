#!/usr/bin/env python
# -*- coding: utf-8 -*-

booleans = ["true", "false"]
operators = ['+', '-', '*']
comparators = ['==', '<=', '<', '>', '>=', '!=']
keywords = ['if', 'then', 'else', 'while', ':=']
separators = ['(', ')', '{', '}', ';']
numbers = [x for x in range(10)]


def is_on():
    # set to True when operational
    return False


def tokenize(program_lines_as_list):
    result = []
    for line in program_lines_as_list:
        result = result + tokenize_line(line)
    return result


def tokenize_line(program_line):
    result = []
    list_words = program_line.split(" ")
    for word in list_words:
        if word in booleans:
            result.append(['boolean', word])
        elif word in operators:
            result.append(['operator', word])
        elif word in comparators:
            result.append(['comparator', word])
        elif word in keywords:
            result.append(['keyword', word])
        elif word.isnumeric():
            result.append(['numeric', word])
        elif word in separators:
            result.append(['separator', word])
        else:
            result.append(['identifier', word])
    return result


def build_blocks(tokens):
    blocks = []

    while len(tokens) != 0:
        # print("tokens remaining:")
        # print(tokens)
        blocks.append(process_list(tokens))

    return blocks


def process_list(tokens):
    new_block = []

    if tokens[0][1] == 'while':
        target = tokens.index(['separator', '}'])
        new_block.extend(tokens[0:target])
        tokens[:] = tokens[target + 1:]
    elif tokens[0][1] == 'if':
        # behaviour depends on if there's an else part
        target_one = tokens.index(['separator', '}'])
        new_block.extend(tokens[0:target_one])
        tokens[:] = tokens[target_one + 1:]
        if tokens[0] == ['keyword', 'else']:
            target_two = tokens.index(['separator', '}'])
            new_block.extend(tokens[0:target_two])
            tokens[:] = tokens[target_two + 1:]

    return new_block


def parse(path_program):
    """
    :param path_program:
    :return: AST tree
    """
    # TODO
    pass


def main():
    with open("./sources_txt/prog_3.txt") as file:
        program = file.read().splitlines()

    tokens = tokenize(program)

    # print('tokens')
    # print(tokens)


    blocks = build_blocks(tokens)

    print('blocks')
    for block in blocks:
        print(block)


    # print('tokens remaining')
    # print(tokens)


# if __name__ == "__main__":
#     main()
