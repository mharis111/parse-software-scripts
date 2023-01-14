
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
        print(node)
        self._name = {'line': node.lineno, 'value': node.s}
        #self.generic_visit(node)

def get_func_calls(tree):
    func_arguments = []
    assignvisitor = AssignVisitor()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for t in node.args:
                if isinstance(t, ast.BinOp):
                    print("rrrrrrrrrrrr")
                    assignvisitor.visit(t.left)
                    func_arguments.append(assignvisitor.name)
                    assignvisitor.visit(t.right)
                    func_arguments.append(assignvisitor.name)
                else:
                    assignvisitor.visit(t)
                    func_arguments.append(assignvisitor.name)
    return func_arguments

def parse_function_arguments(code):
    tree = ast.parse(code)
    print(ast.dump(tree, indent=4))
    return get_func_calls(tree) 
