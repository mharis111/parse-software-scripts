'''
Get all function calls from a python file
The MIT License (MIT)
Copyright (c) 2016 Suhas S G <jargnar@gmail.com>
'''
import ast
from collections import deque
res = []

class AssignVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()


    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)
        res.append({'line': node.lineno, 'target': node.id})

def get_func_calls(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            assignvisitor = AssignVisitor()
            for t in node.targets:
                if isinstance(t, ast.Tuple):
                    for elt in t.elts:
                        assignvisitor.visit(elt)
                else:
                    assignvisitor.visit(t)

def parse_assign_variables(code):
    tree = ast.parse(code)
    get_func_calls(tree)
    return res
