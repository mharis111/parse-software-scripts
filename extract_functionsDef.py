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
        self._name = ''


    @property
    def name(self):
        return self._name

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name = {'line': node.lineno, 'def': node.name}


def get_func_defs(tree):
    func_calls = []
    callvisitor = FuncCallVisitor()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_calls.append(callvisitor.name)
    return func_calls

def parse_functions_defs(code):
    tree = ast.parse(code)
    return get_func_defs(tree)
