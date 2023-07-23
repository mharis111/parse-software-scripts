from csv import DictReader
import ast
import os
import re
import json
import time
import csv
from csv import writer
import requests
import pandas as pd
import os.path

from ExtractRData import *
from parseReadMeFile import *
from ExtractPythonData import *
from ExtractCPPData import *
import glob

def read_extracted_data():
    with open('paper_data new.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        for i in csv_dict_reader:
            print(i['doi'], i['data'])
            for s in ast.literal_eval(i['data']):
                print(s)
            print("-----------------")
        

def read_software_data():
    files=glob.glob('datasets\*.csv')
    count=0
    res = []
    for name in files:
        df = pd.read_csv(name, header=None, usecols=[0,1,2,3])
        df = df.astype("string")
        #print(os.path.splitext(name))
        data=''
        for v in df[2]:
            data = ast.literal_eval(v)
            #for data in ast.literal_eval(v):
                #print(data)
        for v in df[1]:
            p = v.split("/")[0]
            #print(os.path.isdir('temp'+'/'+p))
            for dirpath, dirnames, filenames in os.walk(('temp'+'/'+p)):
                for d in data:
                    head, tail = os.path.split(d)
                    if tail in filenames:
                    #result.append(os.path.join(root, filename))
                        print(tail)
                        res.append(d)
                        count=count+1
    print(len(list(set(res))))
        
            
            
def main():
    #read_software_data()
    read_extracted_data()


if __name__ == "__main__":
    main()
