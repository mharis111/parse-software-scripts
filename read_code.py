
import csv
import ast
from parse_code import parse_ast
from csv import DictReader
from csv import writer
import os
from zipfile import ZipFile
import zipfile
from analyzeCode import extract_datasets
from pathlib import Path
import multiprocessing
import time

res=[]

def is_file_exist(filePath):
    my_file = Path(filePath)
    if my_file.is_file():
        return True
    else:
        return False
        
def is_paper_doi(doi):
    if 'zenodo' not in doi and 'PANGAEA' not in doi and 'dryad' not in doi and 'figshare' not in doi:
        return True

def read_data(repo_name):
    if not (repo_name.endswith('.zip') or repo_name.endswith('.ZIP') or repo_name.endswith('.Zip')):
        return []
    name='figsharesoftware/'+repo_name
    print('name', name)
    files = []
    try:
        with ZipFile(name, 'r') as zipObject:
            with zipfile.ZipFile(name) as zfile:
                zfile.extractall('figsharetemp')
                listOfFileNames = zipObject.namelist()
                for fileName in listOfFileNames:
                    if fileName.endswith('.py') or fileName.endswith('.PY') or fileName.endswith('.ipynb') or fileName.endswith('.IPYNB'):
                        files.append('figsharetemp/'+fileName)
                        #with open('temp/'+fileName) as f:
                        #print(open('temp/'+fileName).read())
    except:
        print("extracting error")
    return files
    
def extract_code(f):
    script = open(f, encoding="ISO-8859-1").read()
    print('file',  f)
    res = parse_ast(script)
    print(res)
    return res
def parse_scripts(doi, repo_name, files):
    astdata = open('figshareastData.csv', 'a', encoding="ISO-8859-1", newline='')
    write_file = csv.writer(astdata)
    for f in files:
        code_semantics = ''
        temp = f
        if f.endswith('.ipynb') or f.endswith('.IPYNB'):
            
            filePath, fileName = os.path.split(temp)
            print('rrrrrr')
            print(filePath)
            head, tail = os.path.splitext(fileName)
            print(head)
            print(tail)
            #pre, ext = os.path.splitext(temp)
            #os.rename(temp, pre + '.py')
            print('9')
            print(filePath+'/'+head+'.py')
            print(is_file_exist(filePath+'/'+head+'.py'))
            if not is_file_exist(filePath+'/'+head+'.py'):
                os.system('jupyter nbconvert --to python '+f)
                #pre, ext = os.path.splitext(f)
                #os.rename(f, pre + '.py')
                f = filePath+'/'+head+'.py'
            if not is_file_exist(f):
                continue

        #script = open(f, encoding="ISO-8859-1").read()
        #print('file',  f)
        #print("-------------")
        try:
            with multiprocessing.Pool(processes=1) as pool:
                result = pool.apply_async(extract_code, (f,))

                res = result.get(timeout=5*60)
            
                code_semantics = extract_datasets(res)
                if 'input_files' in code_semantics and len(code_semantics['input_files'])>0:
                    write_file.writerow([doi, repo_name, temp, code_semantics])
        except:
            print("cannot parsed")

def read_files():
    file_count=0
    count=0
    #softwareData.csv
    with open('figshareData.csv', 'r', encoding="ISO-8859-1") as my_file:
     #passing file object to DictReader()
        csv_dict_reader = DictReader(my_file)
     #iterating over each row
        for i in csv_dict_reader:
            papersDoi = []
            temp = ''
            repo_name=i['repo_url']
            paper_dois = ''
            languages=ast.literal_eval(i['languages']) if i['languages']!='' else ''
            
            paper_dois = ast.literal_eval(i['paper_doi'])
                   
            for j in paper_dois:
                if is_paper_doi(j):
                    papersDoi.append(j)
            if len(papersDoi)>0:        
            #if len(papersDoi)>0 and len(languages)>0 and ('python' in languages or 'Python' in languages or 'ipynb' in languages or 'IPYNB' in languages):
                head, tail = os.path.split(repo_name)
                print(tail)
                files = read_data(tail)
                if len(files) > 0:
                    file_count=file_count+len(files)
                    count=count+1
                    parse_scripts(i['doi'], repo_name, files)
                
    print(file_count)  
    print(count)
    #res = parse_ast(SOURCE)
    #print(res)
def main():
    read_files()
    #download_zenodo_repositories()
    #download_selected_files()
    #get_python_R_packages()


if __name__ == "__main__":
    main()