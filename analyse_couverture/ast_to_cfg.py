# -*- coding: utf-8 -*-
"""CFG Graph Structure:

The CFG Graph is stored as a dictionary.
    Key is the number of the node
    Value is a list containing information about the node:

    Value[0] contains the command type:
    it can be "assign", "while", "if" or "skip"

    ***** "if" and "while" commands:
        Value[1] is the comparator. It can be "<=", ..., ">="

        Value[2] is a length 2 list of values on which the Value[1] operates.
            list[0] is the first value to be compared,
            list[1] the second value
            These two values can either be a string ("x" or "y") or an int

        Value[3] contains a list of 2 integer.
        The first one is the following node when the statement is true,
        the second one the following node when the statement is false.

    ***** "assign" commands:
        Value[1] is a dic {variable: new value}
        Value[2] is the number of the following node

    ***** For "skip" commands:
        Value[1] is the number of the following node

We can see that the ultimate value of the value is always one or more following node.
Value zero represents the _ sign (absence of following node)

An example: graph for "prog" program given in the subject:
graph_prog = {
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '-x'}, 4],
            3: ['assign', {'x': '1-x'}, 4],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, 0],
            6: ['assign', {'x': 'x+1'}, 0]
        }

"""


class AstToCfgConverter(object):
    def __init__(self, ast_tree):
        self.ast_tree = ast_tree
        self.step = 1

    def get_cfg_graph(self):
        # master node must be a sequence
        if self.ast_tree.category == "sequence":
            graph = self.treat_seq_node(self.ast_tree)
            # before returning the graph, we set the last steps to 0 (exit node)
            AstToCfgConverter.set_value_following_node(graph, self.step, 0)
            return graph
        else:
            return None

    @staticmethod
    def set_value_following_node(graph, target_step, new_value):
        for key, value_list in graph.items():
            next_steps = value_list[-1]
            if isinstance(next_steps, list):
                for index, item in enumerate(next_steps):
                    if item == target_step:
                        next_steps[index] = new_value
            else:
                if next_steps == target_step:
                    value_list[-1] = new_value
        return graph

    def treat_seq_node(self, node):
        full_graph = {}
        for child in node.children:
            if child.category == "if":
                partial_graph = self.treat_if_node(child)
                full_graph.update(partial_graph)
                self.step += 1
            elif child.category == "assign":
                tmp = self.treat_assign_node(child)  # ["x+1", ""]
                # 2: ("assign", "-x", "", 4),
                partial_graph = {
                    self.step: ["assign", tmp, self.step + 1]
                }
                full_graph.update(partial_graph)
                self.step += 1
            elif child.category == "while":
                partial_graph = self.treat_while_node(child)
                full_graph.update(partial_graph)
                self.step += 1
            elif child.category == "sequence":
                partial_graph = self.treat_seq_node(child)
                full_graph.update(partial_graph)
                self.step += 1
        return full_graph

    def treat_while_node(self, node):
        operator = self.treat_compare_node(node.children[0])
        while_number_step = self.step
        delta = 1

        # The loop is inside node.children[1].
        # We have to build the graph for this inside loop,
        # and set the exit step to the step number of the while node

        # we have to get the number of steps inside the while loop
        if node.children[1].category == "assign":
            self.step += 1
            delta += 1
            loop_body = self.treat_assign_node(node.children[1])
            # new: replace two places in list by dic
            # to_add = {self.step: ["assign", loop_body[0], loop_body[1], while_number_step]}  # Back to loop
            to_add = {self.step: ["assign", loop_body, while_number_step]}  # Back to loop
        elif node.children[1].category == "sequence":
            self.step += 1
            to_change_before_add = self.treat_seq_node(node.children[1])
            # set last step of sequence to while step number
            self.set_value_following_node(to_change_before_add, self.step, while_number_step)
            # get delta
            delta += len(to_change_before_add)
            to_add = to_change_before_add
        elif node.children[1].category == "if":
            self.step += 1
            to_change_before_add = self.treat_if_node(node.children[1])
            # set last steps of if graph to while step number
            self.set_value_following_node(to_change_before_add, self.step + 1, while_number_step)

            # get delta
            delta += len(to_change_before_add)
            to_add = to_change_before_add
        else:
            to_add = {}

        partial_graph = {while_number_step: ["while",
                                             operator[0],
                                             operator[1],
                                             [while_number_step + 1, while_number_step + delta]]}
        partial_graph.update(to_add)
        return partial_graph

    def treat_if_node(self, node):
        operator = self.treat_compare_node(node.children[0])
        partial_graph = {self.step: ["if", operator[0], operator[1], [self.step+1, self.step+2]]}

        # delta is used to set the number of next step (by default one, could be more for sequence, if, while)
        delta = 1
        if any(node.children[1].category == x for x in ("sequence", "while", "if")):
            if delta < len(node.children[1].children):
                delta = len(node.children[1].children)
        if any(node.children[2].category == x for x in ("sequence", "while", "if")):
            if delta < len(node.children[2].children):
                delta = len(node.children[2].children)

        # left member
        if node.children[1].category == "assign":
            self.step += 1
            if_body_assign = self.treat_assign_node(node.children[1])
            # partial_graph[self.step] = ["assign", if_body_assign[0], if_body_assign[1], self.step + delta + 1]
            # new: replace two places in list by dic
            partial_graph[self.step] = ["assign", if_body_assign, self.step + delta + 1]
        elif node.children[1].category == "sequence":
            self.step += 1
            seq = node.children[1]
            partial_graph.update(self.treat_seq_node(seq))
        elif node.children[1].category == "while":
            self.step += 1
            if_body_while = self.treat_while_node(node.children[1])
            delta = len(if_body_while)
            partial_graph.update(if_body_while)
        elif node.children[1].category == "if":
            self.step += 1
            if_body_if = self.treat_if_node(node.children[1])
            delta = len(if_body_if)
            partial_graph.update(if_body_if)

        # right member
        if node.children[2].category == "assign":
            self.step += 1
            else_body_assign = self.treat_assign_node(node.children[2])
            # partial_graph[self.step] = ["assign", else_body_assign[0], else_body_assign[1], self.step + delta]
            # new: replace two places in list by dic
            partial_graph[self.step] = ["assign", else_body_assign, self.step + delta]
        elif node.children[2].category == "sequence":
            self.step += 1
            seq = node.children[2]
            partial_graph.update(self.treat_seq_node(seq))
        elif node.children[2].category == "while":
            self.step += 1
            else_body_while = self.treat_while_node(node.children[2])
            partial_graph.update(else_body_while)
        elif node.children[2].category == "if":
            self.step += 1
            else_body_if = self.treat_if_node(node.children[2])
            partial_graph.update(else_body_if)

        return partial_graph

    @staticmethod
    def treat_compare_node(node):
        """
        Returns a list [operator(string), [constants]]
        """
        result = [node.data]  # append operator
        values = []

        for child in node.children:
            values.append(child.data)
        
        result.append(values)
        return result

    @staticmethod
    def treat_operation_node(node):
        """
        Returns a string containing the operation
        """
        return str(node.children[0].data) + node.data + str(node.children[1].data)

    @staticmethod
    def treat_assign_node(node):
        """
        Returns a dictionary. Key is the variable, Value is the new affectation
        """
        if node.children[0].category == "constant" or node.children[0].category == "variable":
            left_member_str = str(node.children[0].data)
        else:
            left_member_str = AstToCfgConverter.treat_operation_node(node.children[0])

        if node.children[1].category == "constant" or node.children[1].category == "variable":
            right_member_str = str(node.children[1].data)
        else:
            right_member_str = AstToCfgConverter.treat_operation_node(node.children[1])

        result = {left_member_str: right_member_str}
        return result

    @staticmethod
    def check_children_are_cst_or_var(node):
        for child in node.children:
            if child.category != "constant" and child.category != "variable":
                return False
        return True
