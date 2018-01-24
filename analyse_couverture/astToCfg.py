
class astToCfg(object):
    def __init__(self, astTree):
        self.astTree = astTree
        self.step = 1

    def treat_if_node(self, node):
        operator = self.treat_compare_node(node.children[0])
        partial_graph = {}
        partial_graph[self.step] = ("if", operator[0], operator[1], (self.step+1, self.step+2))

        
        if node.children[1].category == "assign":
            self.step += 1
            if_body_assign = self.treat_assign_node(node.children[1])
            partial_graph[self.step] = ("assign", if_body_assign[0], if_body_assign[1], self.step+2)
        else:
            # TODO
            pass

        if node.children[2].category == "assign":
            self.step += 1
            else_body_assign = self.treat_assign_node(node.children[2])
            partial_graph[self.step] = ("assign", else_body_assign[0], else_body_assign[1], self.step+1)
        else:
            # TODO
            pass

        return partial_graph




    def treat_compare_node(self, node):
        '''
        Returns a list [operator(string), [csts]]
        '''
        result = []
        result.append(node.data) # append operator
        cst = []

        for child in node.children:
            if child.category == "constant":
                cst.append(child.data)
        
        result.append(cst)

        return result

    def treat_operation_node(self, node):
        '''
        Returns a string containing the operation
        '''
        return str(node.children[0].data) + node.data + str(node.children[1].data)

    
    def treat_assign_node(self, node):
        '''
        Returns a list of two elements, the first one being the new affectation of X,
        the second one the new affectation of Y ("" is no new affectation)
        '''
        result = []
        left_member_str = ""
        right_member_str = ""
        if node.children[0].category == "constant" or node.children[0].category == "variable":
            left_member_str = str(node.children[0].data)
        else:
            left_member_str = self.treat_operation_node(node.children[0])

        if node.children[1].category == "constant" or node.children[1].category == "variable":
            right_member_str = str(node.children[1].data)
        else:
            right_member_str = self.treat_operation_node(node.children[1])
        
        if left_member_str == "X" or left_member_str == "x":
            result.append(right_member_str)
            result.append("")
        else:
            result.append("")
            result.append(right_member_str)
        
        return result


def childrenAreCstOrVar(node):
    for child in node.children:
        if child.category != "constant" and child.category !="variable":
            return False
    return True

