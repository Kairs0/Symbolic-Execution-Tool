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
        # result.append('separator')
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
    # TODO wip
    blocks = []
    current_block = []
    for token in tokens:
        if token[0] == 'while':
            current_block.append(token)

    pass


if __name__ == "__main__":
    with open("./sources_txt/prog_3.txt") as file:
        program = file.read().splitlines()

    print(tokenize(program))
