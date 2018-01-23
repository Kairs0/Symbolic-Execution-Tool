class Node(object):
    def __init__(self, category, data=None):
        self.data = data
        self.category = category
        self.value = value
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)