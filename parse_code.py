"""
All the methods were generated based on the list of nodes from the
"Green Tree Snakes" guide:
https://greentreesnakes.readthedocs.io/en/latest/index.html
"""

import ast
from asttree import parse_ast
from extract_functions import parse_functions
from extract_assign import parse_assign_variables
from extract_function_arguments import parse_function_arguments
from extract_assign_values import parse_assign_values

res=[]

def parse_ast(code):
    functions = parse_functions(code)
    assign = parse_assign_variables(code)
    arguments = parse_function_arguments(code)
    values = parse_assign_values(code)
    
    print(functions)
    print(assign)
    print(arguments)
    print(values)
    
