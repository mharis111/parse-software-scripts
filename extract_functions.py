'''
Get all function calls from a python file
The MIT License (MIT)
Copyright (c) 2016 Suhas S G <jargnar@gmail.com>
'''
import ast
from collections import deque

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
        self._name = {'line': node.lineno, 'operation': node.id}

    def visit_Attribute(self, node):
        try:
            self._name = {'line': node.lineno, 'operation': node.value.id+"."+node.attr}
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    callvisitor = FuncCallVisitor()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)
        if isinstance(node, ast.FunctionDef):
            #res.append({'line': node.lineno, 'operation': node.name})
            func_calls.append({'line': node.lineno, 'operation': node.name})
    print(func_calls)
    return func_calls

def parse_functions(code):
    tree = ast.parse(code)
    return get_func_calls(tree)
