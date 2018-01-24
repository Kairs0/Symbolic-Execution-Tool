
class astToCfg(object):
    def __init__(self, astTree):
        self.astTree = astTree


    def treat_compare_node(self, node):
        '''
        Returns a list [operator(string), [csts]]
        '''
        result = []
        result.append(node.data) # append operator
        cst = []

        # while not childrenAreCstOrVar(node):
        #     process(node)

        for child in node.children:
            if child.category == "constant":
                cst.append(child.value)

        return result



def childrenAreCstOrVar(node):
    for child in node.children:
        if child.category != "constant" and child.category !="variable":
            return False
    return True

