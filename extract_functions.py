'''
Get all function calls from a python file
The MIT License (MIT)
Copyright (c) 2016 Suhas S G <jargnar@gmail.com>
'''
import ast
from collections import deque
res = []

class FuncCallVisitor(ast.NodeVisitor):
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
        res.append({'line': node.lineno, 'operation': node.id})

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
            res.append({'line': node.lineno, 'operation': node.value.id+"."+node.attr})
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)

def parse_functions(code):
    tree = ast.parse(code)
    get_func_calls(tree)
    return res
