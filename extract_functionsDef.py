
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
        self._name = {'line': node.lineno, 'def': node.name}


def get_func_defs(tree):
    func_calls = []
    callvisitor = FuncCallVisitor()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_calls.append({'line': node.lineno, 'def': node.name})
    return func_calls

def parse_functions_defs(code):
    tree = ast.parse(code)
    return get_func_defs(tree)
