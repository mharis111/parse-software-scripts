
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
        self._name = {'line': node.lineno, 'target': node.id}

def get_assign_variables(tree):
    assign_variables = []
    assignvisitor = AssignVisitor()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Tuple):
                    for elt in t.elts:
                        assignvisitor.visit(elt)
                        assign_variables.append(assignvisitor.name)
                else:
                    assignvisitor.visit(t)
                    assign_variables.append(assignvisitor.name)
    return assign_variables

def parse_assign_variables(code):
    tree = ast.parse(code)
    return get_assign_variables(tree)
