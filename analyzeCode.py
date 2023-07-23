import pathlib
import pandas as pd


def search_array(value, array):
    if type(value)==list:
        return False
    flag = False
    for v in array:
        if v in value or value in v:
            flag = True
    return flag
    
def find_operation_on_variable(operation, array):
    flag = False
    for v in array:
        if v['op'] in str(operation):
            flag = True
    return flag


def retrieve_function_data(code, name, calling_parameters):
    # print("r", code[name][0]['variable'])
    func_index = -1
    print("--------------------")
    map_name = {}
    for arg in calling_parameters:
        # print(arg)
        if ('def ' + arg) in code.keys():
            func_index = list(calling_parameters).index(arg)
            map_name[code[name][0]['variable'][func_index]] = arg

    for codeLine in code[name]:
        #print('check:', codeLine['op'] if codeLine['op'] not in code.keys() else '')
        if codeLine['op'] not in code.keys() and codeLine['op'] not in functions and codeLine['op'] not in map_name:
            functions.append({'operation': codeLine['op']})
        if codeLine['op'] in map_name:
            functions.append({'operation': map_name[codeLine['op']]})
            print('yes:', map_name[codeLine['op']])
            retrieve_function_data(code, ('def ' + map_name[codeLine['op']]), code[name][0]['variable'])
        # else:
        #    print(codeLine['op'])

    # check parameter type
    # if function is available in keys
    # note the index and the corresponding index will be that function in function definition


def is_valid_file(line):
    file_extension = pathlib.Path(line).suffix
    if len(file_extension) > 1:
        return True
    else:
        return False


def find_input_dataset(code_line):
    if 'loadtxt' in str(code_line['operation']) or 'read_csv' in str(code_line['operation']) or 'genfromtxt' in str(code_line['operation']) or ('open' in str(code_line['operation']) and 'r' in code_line['value'] ):
        return True
    else:
        return False


def find_output_dataset(code_line):
    if ('open' in str(code_line['operation']) and 'a' in code_line['value']) or 'savetxt' in str(code_line['operation']) or 'to_csv' in str(code_line['operation']):
        return True
    else:
        return False
        
def is_assignment_variable(variable, keys, code):
    for line in keys:
        if 'target' in code[line]:
            for a in code[line]['target']:
                if a == variable:
                    return True
    return False

def post_processing(array, code=[]):
    new_array=[]
    for v in array:
        if ',' in v:
            t=v.split(",")
            print(t)
            for t1 in t:
                new_array.append(t1)
        else:
            new_array.append(v)
            print(v)
    if len(code)==0:
        return new_array
    else:
        for line, info in sorted(code.items()):
            if 'target' in info:
                for v in info['target']:
                    if v in new_array:
                        new_array.remove(v)
    return new_array
        
def analyze_code(structured_code):
    operation_variables = []
    file_variable = ''
    for key in structured_code.keys():
        for codeLine in structured_code[key]:
            if find_input_dataset(codeLine):
                input_datasets.append(codeLine['variable'][0])
                if 'target' in codeLine:
                    input_data_variables.append(codeLine['target'])

    for key in structured_code.keys():
        for codeLine in structured_code[key]:
            if find_output_dataset(codeLine):
                output_data.append(codeLine['variable'][0])

    for key in structured_code.keys():
        for codeLine in structured_code[key]:
            if 'op' in codeLine:
                if search_array(codeLine['op'], input_data_variables):
                    if 'target' in codeLine:
                        operation_variables.append(codeLine['target'])
                functions.append(codeLine['op'])

            if 'variable' in codeLine:
                for v in codeLine['variable']:
                    if search_array(v, input_data_variables):
                        operation_variables.append(v)
                        functions.append(codeLine['op'])
                functions.append(codeLine['op'])
        '''
        for codeLine in structured_code[key]:
            if find_input_dataset(codeLine):
                if codeLine['variable'] not in functions:
                    functions.append({'input dataset': codeLine['variable'][0]})
                print('input dataset:', codeLine['variable'])
                operation_variables.append(codeLine['target'])
            #print(codeLine)

            if find_output_dataset(codeLine):
                print('output dataset:')
                [functions.append({'output dataset': fl} if fl not in functions else '') if is_valid_file(fl) else '' for fl in codeLine['variable']]

    #print(operation_variables)
    #print(functions)

    for i in operation_variables:
        if i in codeLine['variable']:
            print('op:', codeLine['op'])
            if codeLine['op'] not in functions and codeLine['op'] != '':
                functions.append({'operation': codeLine['op']})
            if codeLine['op'] != '' and (('def ' + codeLine['op']) in structured_code.keys()):
                retrieve_function_data(structured_code, ('def ' + codeLine['op']), codeLine['variable'])
            operation_variables.append(codeLine['target'])


    print("output...")
    for n, i in enumerate(functions):
        if i not in functions[n + 1:]:
                print(i)
    '''
    print("input data:")
    combine_keywords = []
    print(input_datasets)
    for i in input_datasets:
        combine_keywords.append(i.lower())
    for n, i in enumerate(operation_variables):
        if i not in operation_variables[n + 1:]:
            print(i)
            combine_keywords.append(i.lower())

    for n, i in enumerate(functions):
        if i not in functions[n + 1:]:
            print(i)
            combine_keywords.append(i.lower())
    for i in output_data:
        combine_keywords.append(i.lower())
    print(output_data)
    print(combine_keywords)
    return combine_keywords
    
    
def extract_datasets(code):
    print("rrrrrrrrrrrrrr")
    functions = []
    input_data = []
    input_files = []
    output_files = []
    output_data = []
    sorted_code = sorted(code.keys())
    # find input datasets
    for line in sorted_code:
        print(line, code[line])
        # if operation is done in the line
        if 'operation' in code[line]:
            # if operation is reading file
            if find_input_dataset(code[line]):
                print('input file name', code[line]['value'])
                if 'target' in code[line]:
                    print('target', code[line]['target'])
                    functions.append({'line': line, 'op': ','.join(code[line]['target'])})
                    input_data.append(','.join(code[line]['operation']))
                    input_files.append(','.join(code[line]['value']))
            elif find_output_dataset(code[line]):
                print('output file name', code[line]['value'])
                output_data.append(','.join(code[line]['operation']))
                output_files.append(','.join(code[line]['value']))
                                   
    for line in sorted_code:
        if 'operation' in code[line]:
            if find_operation_on_variable(code[line]['operation'], functions):
                if 'operation' in code[line]:
                    print('operation', code[line]['operation'])
                    functions.append({'line': line, 'op': ','.join(code[line]['operation'])})
                if 'target' in code[line]:
                    functions.append({'line': line, 'op': ','.join(code[line]['target'])})
        
        if 'value' in code[line]:
            if find_operation_on_variable(code[line]['value'], functions):
                if 'operation' in code[line]:
                    functions.append({'line': line, 'op': ','.join(code[line]['operation'])})
                if 'target' in code[line]:
                    functions.append({'line': line, 'op': ','.join(code[line]['target'])})
    print(functions)
    temp = []
    for f in functions:
        arr = f['op'].split(".")
        if len(arr) > 0:
            temp.append({'line': f['line'], 'op': arr[0]})      
    
    for line in sorted_code:
        if 'target' in code[line]:
            if find_operation_on_variable(code[line]['target'], temp):
                if 'operation' in code[line]:
                    functions.append({'line': line, 'op': ','.join(code[line]['operation'])})
            
    #functions = sorted(functions, key = lambda x : x["line"], reverse= False)
    temp = []
    print(input_data)
    print(output_data)
    for f in functions:
        if f['op'] not in temp and not is_assignment_variable(f['op'], sorted_code, code) and f['op'] not in input_data and f['op'] not in output_data:
        #if f['op'] not in temp:
            temp.append(f['op'])
    print(input_files)  
    print(temp)
    print(output_files)
    return {'input_files': post_processing(input_files), 'operations': post_processing(temp, code), 'output_files': post_processing(output_files)}
            
            
    