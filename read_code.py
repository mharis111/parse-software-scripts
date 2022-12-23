"""
All the methods were generated based on the list of nodes from the
"Green Tree Snakes" guide:
https://greentreesnakes.readthedocs.io/en/latest/index.html
"""

import ast
from parse_code import parse_ast

res=[]

if __name__ == "__main__":
    SOURCE = """
r = 9
r = x
r = m[9]
"""
    res = parse_ast(SOURCE)
    print(res)