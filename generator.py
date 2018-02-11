#!/usr/bin/env python
# -*- coding: utf-8 -*-


def all_affectations(graph):
    objective = []
    for key, value in graph.items():
        if value[0] == "assign":
            objective.append(key)

    for step in objective:
        # get_path_to_get_there
        # get_father_for_node
        pass