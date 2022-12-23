
import os.path

from zipfile import ZipFile
import zipfile
import glob

import sys
import shutil
from csv import DictReader
import ast
import os
import re
import json
import time
import csv
from csv import writer
import sys
maxInt = sys.maxsize
 
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
 
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

with open('paper_data new.csv', 'r', encoding="utf-8") as my_file:
    # passing file object to DictReader()
    csv_dict_reader = DictReader(my_file)
    # iterating over each row
    repository_name = ''
    terms_length=0
    python_files=0
    package=0
    python_paper_package=0
    count=0
    for i in csv_dict_reader:
        doi=''
        sk=''
        repos=[]
        flag = False
        data = ast.literal_eval(i['data']) if i['data'] != '' else ''
        #print(data)
        if len(data) ==0:
            print(data)
            count=count+1
        print("-----------")
    print(count)
        