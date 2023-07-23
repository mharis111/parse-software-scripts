from csv import DictReader
import ast
import os
import re
import json
import time
import csv
from csv import writer
import requests
import os.path
from difflib import SequenceMatcher
from orkg import ORKG
from sentence_transformers import SentenceTransformer, util
import torch
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
from nltk.util import ngrams
from nltk import word_tokenize
embedder = SentenceTransformer('all-MiniLM-L6-v2')
orkg = ORKG(host="https://sandbox.orkg.org/", creds=('Muhammad.Haris@tib.eu', 'Qwerty.123'))
import pandas as pd
import json
import matplotlib.pyplot as plt
from collections import Counter


def remove_special_characters(s):
    #print('s', s)
    special_characters = ['!', '#', '$', '%', '&',  '@', '[', ']', "'", '{', '}', '"', ',', '*', ')', '(', '<', '-', ':']
    a2 = ''
    for i in s:
        if i=='_':
            a2 = a2+' '
        elif i not in special_characters:
            a2 = a2 + i
    if len(a2)>0:
        if a2[len(a2)-1] in '.' or a2[len(a2)-1] in '/':
            a2=a2[:-1]
    return a2
    

def is_valid_file(file_name):
    if '.txt' in file_name or '.csv' in line or '.json' in line or '.xlsx' in line or '.xml' in line:
        return True
    return False
    
def get_file_extension(file_name):
    name, extension=os.path.splitext(file_name)
    return extension

def is_paper_doi(doi):
    if 'zenodo' not in doi and 'PANGAEA' not in doi and 'dryad' not in doi and 'figshare' not in doi:  
        return True
    return False 

def concate_string(string):
    temp=''
    for v in string:
        temp=temp+"_"+v.lower()
    return temp[1:]
    

    
def is_file_exist_in_directory(path, file_name):
    folders=path.split('/')
    root=folders[0]+'/'+folders[1]
    #print(root)
    for dirpath, dirnames, filenames in os.walk(root):
        head, tail = os.path.split(file_name)
        if tail in filenames:
            #print(dirpath)
            #result.append(os.path.join(root, filename))
            #print(tail)
            return True
    return False
    
def ttest_template(tp, file_name, value):
    i=0
    df = pd.read_csv('experimental_dataset_N60.csv', header=i)
    #rr = DictReader(r)
    tp = orkg.templates
    instance=tp.students_ttest(
    label='ttest',
    has_dependent_variable='', # the study design dependent variable
    has_specified_input=(df, file_name),
    has_specified_output=tp.pvalue('p-value', tp.scalar_value_specification(str(value), value)),
)#.serialize_to_file('article.contribution.1.json', format="json-ld")
    #instance.pretty_print()
    instance.save()

    
    
def get_orkg_templates():
    t = []
    #orkg.templates.materialize_templates()
    response = requests.get('https://orkg.org/api/classes/ContributionTemplate/resources/?desc=true&page=0&size=500').json()['content']
    #print(response)
    for r in response:
        #print(r['label'])
        t.append({'label': remove_special_characters(r['label']), 'id': r['id']})
    return t
    

def read_code_semantics():
    t=get_orkg_templates()
    tp=orkg.templates.materialize_templates()
    #embed=create_corpus_embeddings(t)
    count=0
    temp=[]
    datasets_used=0
    extracted_data={}
    papers = []
    file = pd.read_csv('scholarly_knowledge.csv', header=0)
    file = file.groupby('paper_doi')
    
    for key, value in file:
        print(key)
        inputData = []
        operations = []
        outputData = []
        for code_semantics in value['parsed_code']:
            code_semantics = ast.literal_eval(code_semantics)
            input_data = list(set(code_semantics['input_files']))
            operations = list(set(code_semantics['operations']))
            output_data = list(set(code_semantics['output_files']))
            code_result = value['code_result']
            #code_result = ast.literal_eval(value['code_result']) if value['code_result'] != 'NaN' else ''
            print(input_data)
            for e in code_result:
                if not pd.isna(e):
                    print(e)
                    
                    #for v in t:
                        #r = v['label'].split(' ')
                        #if e['label'] in r:
                            #print(e['label'], v['id'])
                            #tp=orkg.templates.materialize_template(v['id'])
                            #tname=concate_string(r)
                            #template=getattr(orkg.templates, tname)
                            #print(template.__doc__)
                            #ttest_template(tp)
                            #return
        
            for dataset_name in input_data: 
                extension=get_file_extension(dataset_name)
                if extension !='':
                    if True: #is_file_exist_in_directory(file_name, dataset_name):
                        papers.append(key)
                        count=count+1
                        operations.append(operations)
                        inputData.append(dataset_name)
                    else:
                        operations.append(operations)
            
            for dataset_name in output_data: 
                extension=get_file_extension(dataset_name)
                if extension !='':
                    outputData.append(dataset_name)
                    
        print(inputData)
        print(operations)
        print(outputData)
        print('-----')
        
    
                        
    
    print(count)
    print(len(list(set(papers))))
    return extracted_data
    
def read_code():
    t=get_orkg_templates()
    orkg.templates.materialize_templates()
    #embed=create_corpus_embeddings(t)
    count=0
    temp=[]
    datasets_used=0
    extracted_data={}
    papers = []
    file = open('scholarly_knowledge.csv', 'r', encoding="ISO-8859-1")
    csv_dict_reader = DictReader(file)
    for i in csv_dict_reader:
        sd = i['doi']
        doi = i['paper_doi']
        fn = i['file_name']
        code = ast.literal_eval(i['parsed_code'])
        result = i['code_result']
        if doi not in extracted_data.keys():
            extracted_data[doi] = []
        else:
            extracted_data[doi].append({'input': code['input_files'], 'op': code['operations'], 'output': code['output_files']})
    
    print(extracted_data['10.1038/s41563-017-0007-z'])
        
def generate_histogram():
    file = pd.read_csv('scholarly_knowledge.csv', header=0)
    #file = file.groupby('paper_doi')
    #code = ast.literal_eval(file['parsed_code'])
    operations = []
    for value in file['parsed_code']:
        value = ast.literal_eval(value)
        #print(value['operations'])
        for r in value['operations']:
            operations.append(r)
    #print(operations)
    
    letter_counts = Counter(operations)
    df = pd.DataFrame.from_dict(letter_counts, orient='index')
    df.plot(kind='bar')
    plt.show()
    
            
def main():
    read_code()
    #generate_histogram()
 


if __name__ == "__main__":
    main()
