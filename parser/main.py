booleans = ["true", "false"]
operators = ['+', '-', '*']
comparators = ['==', '<=', '<', '>', '>=']
keywords = ['if', 'then', 'else', 'while', ':=']


def tokenize(program_lines_as_list):
    result = []
    for line in program_lines_as_list:
        result = result + tokenize_line(line)
        result.append('separator')
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
        else:
            result.append(['identifier', word])

    return result


if __name__ == "__main__":
    with open("../analyse_couverture/sources_txt/prog_3.txt") as file:
        program = file.read().splitlines()

    print(tokenize(program))
