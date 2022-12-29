"""
All the methods were generated based on the list of nodes from the
"Green Tree Snakes" guide:
https://greentreesnakes.readthedocs.io/en/latest/index.html
"""

import ast
from extract_functions import parse_functions
from extract_functionsDef import parse_functions_defs
from extract_assign import parse_assign_variables
from extract_function_arguments import parse_function_arguments
from extract_assign_values import parse_assign_values
import numpy as np

res=[]

def create_list(code, parameter, combined_result):
    line_visited = []
    p = []
    for line in code:
        line_no = line['line']
        if line_no not in line_visited:
            line_visited.append(line_no)
            p = []
        if line_no not in combined_result:
            combined_result[line['line']] = {}
        else:
            if parameter in combined_result[line['line']]:
                p = combined_result[line['line']][parameter]
        
        p.append(line[parameter])
        combined_result[line_no].update({parameter: p})
    return combined_result
                #if key == parameter:
                 #   combined_result[line_no].update({key: p})

def combine_parsed_data(function_nodes, functions_defs, assign_nodes, argument_nodes, value_nodes):
    combined_result = {}
    node_lengths = [{"name": function_nodes, "parameter": "operation", "length": len(function_nodes)},
        {"name": assign_nodes, "parameter": "target", "length": len(assign_nodes)},
        {"name": argument_nodes, "parameter": "value", "length": len(argument_nodes)},
        {"name": value_nodes, "parameter": "value", "length": len(value_nodes)},
        {"name": functions_defs, "parameter": "def", "length": len(functions_defs)}]
        
    node_lengths = sorted(node_lengths, key = lambda x : x["length"], reverse= True)
    for node in node_lengths:
        combined_result = create_list(node["name"], node["parameter"], combined_result)
    #create_list(function_nodes, "operation")
    #create_list(assign_nodes, "target")
    #create_list(argument_nodes, "value")
    #create_list(value_nodes, "value")
    
    for line in sorted(combined_result.keys()):
        print(line, combined_result[line])
    return combined_result

def parse_ast(code):
    functions = parse_functions(code)
    functions_defs = parse_functions_defs(code)
    assign = parse_assign_variables(code)
    arguments = parse_function_arguments(code)
    values = parse_assign_values(code)
    
    #print("function")
    #print(functions)
    #print("assign")
    #print(assign)
    #print("argument")
    #print(arguments)
    #print("value")
    #print(values)
    #print("functions defs")
    #print(functions_defs)
    
    combine_parsed_data(functions, functions_defs , assign, arguments, values)
    #print(combined_result)
    
