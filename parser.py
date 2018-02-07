from collections import deque

booleans = ["true", "false"]
operators = ['+', '-', '*']
comparators = ['==', '<=', '<', '>', '>=', '!=']
keywords = ['if', 'then', 'else', 'while', ':=', 'end']
separators = ['(', ')', '{', '}', ';']
numbers = [x for x in range(10)]


def tokenize(program_lines_as_list):
    result = []
    for line in program_lines_as_list:
        result = result + tokenize_line(line)
    return result


def tokenize_v2(program_lines_as_list):
    result = deque()
    for line in program_lines_as_list:
        result.extendleft(tokenize_line_v2(line))
    return result


def tokenize_line_v2(program_line):
    result = deque()
    list_words = program_line.split(' ')
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
        blocks.append(process_list(tokens))

    return blocks


def process_list(tokens):
    new_block = []
    target = 0
    if tokens[0][1] == 'while':
        target = tokens.index(['separator', '}'])
        new_block.extend(tokens[0:target])

    if tokens[0][1] == 'if':
        # behaviour depends on if there's an else part

        pass  # TODO

    tokens[:] = tokens[target + 1:]
    return new_block


def main():
    with open("./sources_txt/prog_3.txt") as file:
        program = file.read().splitlines()

    tokens = tokenize(program)

    print('tokens')
    print(tokens)

    print('blocks (here block 2')
    blocks = build_blocks(tokens)
    print(blocks[1])

    print('tokens remaining')
    print(tokens)


if __name__ == "__main__":
    main()
