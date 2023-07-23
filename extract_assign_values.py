
import ast
from collections import deque

class AssignValuesVisitor(ast.NodeVisitor):
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
        self.generic_visit(node)
        
    def visit_Constant(self, node):
        self._name = {'line': node.lineno, 'value': node.s}
        self.generic_visit(node)
        
    def visit_Attribute(self, node):
        try:
            self._name = {'line': node.lineno, 'value': node.value.id+"."+node.attr}
        except AttributeError:
            pass

def get_assign_values(tree):
    assignvaluesvisitor = AssignValuesVisitor()
    assign_values = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            print("rrrrrrrrrrrr")
            print(tree)
            if isinstance(node.value, ast.Name):
                assignvaluesvisitor.visit(node.value)
                assign_values.append(assignvaluesvisitor.name)
            if isinstance(node.value, ast.Constant):
                assignvaluesvisitor.visit(node.value)
                assign_values.append(assignvaluesvisitor.name)
            if isinstance(node.value, ast.Attribute):
                assignvaluesvisitor.visit(node.value)
                assign_values.append(assignvaluesvisitor.name)
            if isinstance(node.value, ast.Subscript):
                for subnode in ast.walk(node.value):
                    if isinstance(subnode, ast.Name):
                        assignvaluesvisitor.visit(subnode)
                        assign_values.append(assignvaluesvisitor.name)
            if isinstance(node.value, ast.BinOp):
                assignvaluesvisitor.visit(node.value)
                assign_values.append(assignvaluesvisitor.name)
    return assign_values

def parse_assign_values(code):
    tree = ast.parse(code)
    return get_assign_values(tree)
