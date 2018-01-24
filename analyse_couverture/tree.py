
class Node(object):
    def __init__(self, category, data=None):
        self.data = data
        self.category = category
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def calc_level(self):
        rec_calc_level(self, 0)

    def getHeight(self):
        self.calc_level()
        h = 0
        for n in get_all_nodes_and_leaves(self):
            if n.level > h:
                h = n.level

        return h

    def print_me(self):
        h = self.getHeight()
        tree_list = get_all_nodes_and_leaves(self)
        to_print = []
        for i in range(h):
            to_print.append([])
            for node in tree_list:
                if node.level == i:
                    to_print[i].append(node)

        for nodes_list in to_print:
            for node in nodes_list:
                print(node.category, end='-')
            print("\n|")


def get_all_nodes_and_leaves(node):
    result = []
    result.append(node)
    if len(node.children) == 0:
        return result
    else:
        for child in node.children:
            result = result + get_all_nodes_and_leaves(child)
    return result


def rec_calc_level(node, lvl):
    node.level = lvl
    for child in node.children:
        rec_calc_level(child, lvl + 1)