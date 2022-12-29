'''
Get all function calls from a python file
The MIT License (MIT)
Copyright (c) 2016 Suhas S G <jargnar@gmail.com>
'''
import ast
from collections import deque

class AssignVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = ''


    @property
    def name(self):
        return self._name

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name = {'line': node.lineno, 'value': node.id} 
        
    def visit_Constant(self, node):
        self._name = {'line': node.lineno, 'value': node.s}
        self.generic_visit(node)

def get_func_calls(tree):
    func_arguments = []
    assignvisitor = AssignVisitor()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for t in node.args:
                assignvisitor.visit(t)
                func_arguments.append(assignvisitor.name)
    return func_arguments

def parse_function_arguments(code):
    tree = ast.parse(code)
    return get_func_calls(tree) 
