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
        Value[1] is a dic {variable: new value}, (keys and values are string, eg {'x': '4'}
        Value[2] is the number of the following node (list)

    ***** For "skip" commands:
        Value[1] is the number of the following node (list)

We can see that the ultimate value of the value is always one or more following node.
Value zero represents the _ sign (absence of following node)

An example: graph for "prog" program given in the subject:
graph_prog = {
            1: ['if', '<=', ["x", 0], [2, 3]],
            2: ['assign', {'x': '-x'}, [4]],
            3: ['assign', {'x': '1-x'}, [4]],
            4: ['if', '==', ["x", 1], [5, 6]],
            5: ['assign', {'x': '1'}, [0]],
            6: ['assign', {'x': 'x+1'}, [0]]
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
            # before returning the graph, we check for any inconsistencies like
            # node jumping a step (passing from step 3 to 5 for example),
            # and if it is the case we clean the graph
            # can occur when we have sequence while nested in the if of the sequence,
            # or others cases like that
            graph = AstToCfgConverter.clean_inconsistent_graph(graph)
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

    @staticmethod
    def clean_inconsistent_graph(graph):
        """
        If there is missing nodes or shifted nodes in the graph,
        will shift every wrong based node.
        Otherwise, returns the graph
        :param graph:
        :return: clean graph
        """
        # if their is missing nodes of shifted node in the graph,
        # will shift every wrong based node.
        # Otherwise, returns the graph
        initial_keys = []
        for key, value_list in graph.items():
            initial_keys.append(key)

        bigger_key = max(initial_keys)

        error = 0
        # loop through the keys to see if there is any missing
        for i in range(1, bigger_key):
            if i not in initial_keys:
                error = i

        if error == 0:
            return graph

        # make sub graph of keys to modify, shifting the keys number already
        sub_graph = {key - 1: graph[key] for key in graph if key > error}

        # shift values for all values inside each node (including last one) from n to n-1
        for j in range(error, bigger_key + 1):
            AstToCfgConverter.set_value_following_node(sub_graph, j, j-1)
            if j < bigger_key:
                graph.pop(j+1)

        graph.update(sub_graph)
        # recursive call to clean if their was an other error
        return AstToCfgConverter.clean_inconsistent_graph(graph)

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
                    self.step: ["assign", tmp, [self.step + 1]]
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
            to_add = {self.step: ["assign", loop_body, [while_number_step]]}  # Back to loop
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

        # delta is used to set the number of next step (by default one, and more for sequence, if, while)
        delta = 1
        delta_left = 2
        delta_right = 1
        if any(node.children[1].category == x for x in ("sequence", "while", "if")):
            length_child_node = AstToCfgConverter.get_length_node(node.children[1])
            delta_left = 1 + length_child_node
            if delta < length_child_node:
                delta = length_child_node

        if any(node.children[2].category == x for x in ("sequence", "while", "if")):
            length_child_node = AstToCfgConverter.get_length_node(node.children[2])
            delta_right = length_child_node
            if delta < length_child_node:
                delta = length_child_node

        right_value_next_step = self.step + delta_left
        partial_graph = {self.step: ["if", operator[0], operator[1], [self.step + 1, right_value_next_step]]}

        # left member
        if node.children[1].category == "assign":
            self.step += 1
            if_body_assign = self.treat_assign_node(node.children[1])
            partial_graph[self.step] = ["assign", if_body_assign, [self.step + delta + 1]]
        elif node.children[1].category == "sequence":
            self.step += 1
            seq = node.children[1]
            partial_graph.update(self.treat_seq_node(seq))
        elif node.children[1].category == "while":
            self.step += 1
            if_body_while = self.treat_while_node(node.children[1])
            AstToCfgConverter.set_value_following_node(
                if_body_while, self.step + 1, right_value_next_step + delta_right
            )
            partial_graph.update(if_body_while)
        elif node.children[1].category == "if":
            self.step += 1
            if_body_if = self.treat_if_node(node.children[1])
            partial_graph.update(if_body_if)

        # right member
        if node.children[2].category == "assign":
            self.step += 1
            else_body_assign = self.treat_assign_node(node.children[2])
            partial_graph[self.step] = ["assign", else_body_assign, [self.step + 1]]
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

    @staticmethod
    def get_length_node(node):
        if node.category == "sequence":
            return AstToCfgConverter.get_length_sequence(node)
        elif node.category == "if":
            return AstToCfgConverter.get_length_if(node)
        elif node.category == "while":
            return AstToCfgConverter.get_length_while(node)
        else:
            return 1

    @staticmethod
    def get_length_if(node):
        # TODO maybe not correct (what is the "length" of a if?)
        if node.children[1] == "sequence":
            length_if_body = AstToCfgConverter.get_length_sequence(node.children[1])
        elif node.children[1] == "while":
            length_if_body = AstToCfgConverter.get_length_while(node.children[1])
        elif node.children[1] == "if":
            length_if_body = AstToCfgConverter.get_length_if(node.children[1])
        else:
            length_if_body = 1

        if node.children[2] == "sequence":
            length_else_body = AstToCfgConverter.get_length_sequence(node.children[2])
        elif node.children[2] == "while":
            length_else_body = AstToCfgConverter.get_length_while(node.children[2])
        elif node.children[2] == "if":
            length_else_body = AstToCfgConverter.get_length_if(node.children[2])
        else:
            length_else_body = 1
        # TODO understand why 2 is correct
        return 2 + max(length_if_body, length_else_body)

    @staticmethod
    def get_length_while(node):
        if node.children[1] == "sequence":
            length_body = AstToCfgConverter.get_length_sequence(node.children[1])
        elif node.children[1] == "while":
            length_body = AstToCfgConverter.get_length_while(node.children[1])
        elif node.children[1] == "if":
            length_body = AstToCfgConverter.get_length_if(node.children[1])
        else:
            length_body = 1
        return 1 + length_body

    @staticmethod
    def get_length_sequence(node):
        if all(child != long_cat for child in node.children for long_cat in ("sequence", "while", "if")):
            return len(node.children)
        else:
            length = 0
            for child in node.children:
                if child.category == "sequence":
                    length += AstToCfgConverter.get_length_sequence(child)
                elif child.category == "if":
                    length += AstToCfgConverter.get_length_if(child)
                elif child.category == "while":
                    length += AstToCfgConverter.get_length_while(child)
            return length
