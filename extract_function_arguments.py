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
        res.append({'line': node.lineno, 'value': node.id})
        
    def visit_Constant(self, node):
        print(self)
        print(node.end_lineno)
        res.append({'line': node.lineno, 'value': node.s})
        self.generic_visit(node)

def get_func_calls(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assignvisitor = AssignVisitor()
            for t in node.args:
                assignvisitor.visit(t)

def parse_function_arguments(code):
    tree = ast.parse(code)
    get_func_calls(tree)
    return res
