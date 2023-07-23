import requests
import os.path
from zipfile import ZipFile
import zipfile
import time
from pathlib import Path
import csv
from csv import writer
from csv import DictReader
import ast
import importlib  
from analyzeCode import extract_datasets
from parse_code import parse_ast

def is_file_exist(filePath):
    my_file = Path(filePath)
    if my_file.is_file():
        return True
    else:
        return False

ACCESS_TOKEN = '123456'

date_ranges=[{'s': '2015-01-01', 'e': '2015-05-01'},
{'s': '2015-05-02', 'e': '2015-09-01'},
{'s': '2015-09-02', 'e': '2016-01-01'},
{'s': '2016-01-02', 'e': '2016-05-01'},
{'s': '2016-05-02', 'e': '2016-09-01'},
{'s': '2016-09-02', 'e': '2017-01-01'},
{'s': '2017-01-02', 'e': '2017-05-01'},
{'s': '2017-05-02', 'e': '2017-09-01'},
{'s': '2017-09-02', 'e': '2018-01-01'},
{'s': '2018-01-02', 'e': '2018-05-01'},
{'s': '2018-05-02', 'e': '2018-09-01'},
{'s': '2018-09-02', 'e': '2019-01-01'},
{'s': '2019-01-02', 'e': '2019-05-01'},
{'s': '2019-05-02', 'e': '2019-09-01'},
{'s': '2019-09-02', 'e': '2020-01-01'},
{'s': '2020-01-02', 'e': '2020-05-01'},
{'s': '2020-05-02', 'e': '2020-09-01'},
{'s': '2020-09-02', 'e': '2021-01-01'},
{'s': '2021-01-02', 'e': '2021-05-01'},
{'s': '2021-05-02', 'e': '2021-09-01'},
{'s': '2021-09-02', 'e': '2022-01-01'},
{'s': '2022-01-02', 'e': '2022-05-01'},
{'s': '2022-05-02', 'e': '2022-09-01'},
{'s': '2022-09-02', 'e': '2023-01-01'}]

# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
    
#2015-01-01 2015-05-01
#2015-05-02 2015-09-01
#2015-09-02 2016-01-01

#2016-01-02 to 2016-05-01
#2016-05-02 to 2016-09-01
#2016-09-02 to 2017-01-02


def create_date_ranges():
    start_year = 2015
    start_month = 1
    start_day = 1
    end_year = 2023
    r = []
    start = ''
    end = ''
    while start_year < end_year:
        # 3 intervals in a year
        i=0
        m = 1
        start_day = 1
        #print(start_year, i, start_day)
        while i <=12 and start_year < end_year:
            print(str(start_year)+"-"+str(m)+"-"+str(1))
            start = str(start_year)+"-"+str(m)+"-"+str(1)
            m = m+4
            if(m > 12):
                print("r")
                m=1
                start_year = start_year+1
                end = str(start_year)+"-"+str(m)+"-"+str(1)
                print(str(start_year)+"-"+str(m)+"-"+str(1))
                m = 1
            
            else:
                print("rr")
                end = str(start_year)+"-"+str(m)+"-"+str(1)
                print(str(start_year)+"-"+str(m)+"-"+str(1))
                i=1
            print("-----------")
            r.append({'s': start, 'e': end})
            start_day=2
            #m=m+4
            i = i+4
            if start_year == 2023:
                break
    print(r)
        #start_year = start_year+1
    


def get_python_R_packages():
    with open('softwareData.csv', 'r', encoding="ISO-8859-1") as my_file, open('softwarePackages.csv', 'a', encoding="utf-8", newline='') as write_file:
        writer = csv.writer(write_file)
        csv_dict_reader = DictReader(my_file)
        writer.writerow(['software_doi', 'paper dois', 'languages', 'zenodo_url'])
        repository_name = ''
        count=0
        repos=[]
        for i in csv_dict_reader:
            repository_name = i['repository_name']
            head, tail = os.path.split(i['zenodo_url'])
            #print(repository_name)
            print('---------')
            flag = False
            languages = ast.literal_eval(i['languages']) if i['languages'] != '' else ''
            if i['paper_doi'] != '' and repository_name not in repos:
                if i['paper_doi'][0] == '[':
                    paper_dois = ast.literal_eval(i['paper_doi'])
                    for pdoi in paper_dois:
                        count = count+1
                        if 'zenodo' not in pdoi and 'PANGAEA' not in pdoi and 'dryad' not in pdoi and 'figshare' not in pdoi and (
                                'python' in languages or 'Python' in languages):
                            flag = True
                        else:
                            paper_dois = i['paper_doi']
                            #print(i['paper_doi'])
                            if 'zenodo' not in paper_dois and 'PANGAEA' not in paper_dois and 'dryad' not in paper_dois and 'figshare' not in paper_dois and (
                                    'python' in languages or 'Python' in languages):
                                flag = True
                        
                        if flag and i['doi'] not in repos:
                            repos.append(i['doi'])
                            #print(i['doi'], paper_dois, languages)
                            writer.writerow([i['doi'], paper_dois, languages, i['zenodo_url']])
        print(count)
        print(repos)
      
def is_paper_doi(doi):
    if 'zenodo' not in doi and 'PANGAEA' not in doi and 'dryad' not in doi and 'figshare' not in doi:
        return True

def download_python_files():
    with open('softwareData.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        count = 0
        visited_doi = []
        for i in csv_dict_reader:
            flag = False
            repository_name = i['repository_name']
            head, tail = os.path.split(i['zenodo_url'])
            #print(repository_name)
            languages = ast.literal_eval(i['languages']) if i['languages'] != '' else ''
            #if 'python' in languages or 'Python' in languages:
                #print(languages)
                #print("")
            if i['paper_doi'] != '' and ('Python' in languages or 'python' in languages):
                if i['paper_doi'][0] == '[': 
                    paper_dois = ast.literal_eval(i['paper_doi'])
                    for doi in paper_dois:
                        if is_paper_doi(doi) and doi not in visited_doi:
                            #print(doi)
                            count = count+1
                            visited_doi.append(doi)
                            flag = True
                else:
                    if is_paper_doi(i['paper_doi']) and i['paper_doi'] not in visited_doi:
                        #print(i['paper_doi'])
                        #print("r")
                        count = count+1
                        visited_doi.append(doi)
                        flag = True
                
                if flag and not is_file_exist("downloadedFiles/" + tail):
                    print(i['zenodo_url'])
                    print(count)
                    wget.download(i['zenodo_url'], out="D:\knowledge extraction\downloadedFiles")
                else:
                    print('file already exist')
                    
                    
    print(count)
    
def parse_scripts(doi, repo_name, files):
    astdata = open('astData-figshare.csv', 'a', encoding="ISO-8859-1", newline='')
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

        script = open(f, encoding="ISO-8859-1").read()
        print('file',  f)
        #print("-------------")
        try:
            res = parse_ast(script)
            print(res)
            code_semantics = extract_datasets(res)
            if 'input_files' in code_semantics and len(code_semantics['input_files'])>0:
                write_file.writerow([doi, repo_name, temp, code_semantics])
        except:
            print("cannot parsed")
    
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
                        print(fileName)
                        files.append('figsharetemp/'+fileName)
                        #with open('temp/'+fileName) as f:
                        #print(open('temp/'+fileName).read())
    except:
        print("extracting error")
    return files
    
def parse_figshare_python_packages():
    with open('figsharesoftwarepackages.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        repository_name = ''
        count=0
        file_count=0
        repos=[]
        for i in csv_dict_reader:
            doi = i['software_doi']
            title=i['title']
            paper_doi=i['paper_doi']
            file_name=i['file_name']
            flag = False
            if paper_doi!='':
                print(paper_doi)
                files=read_data(file_name)
                if len(files) > 0:
                    file_count=file_count+len(files)
                    #parse_scripts(doi, file_name, files)
                #writer.writerow([doi, title, paper_doi, file_name, 'python'])
                    count=count+1
            #print('------')
            
        print(file_count)
        print(count)
        print(repos)         

def filter_python_figshare_packages():
    with open('figshareData.csv', 'r', encoding="ISO-8859-1") as my_file, open('figsharesoftwarePackages.csv', 'a', encoding="utf-8", newline='') as write_file:
        writer = csv.writer(write_file)
        csv_dict_reader = DictReader(my_file)
        writer.writerow(['software_doi', 'title', 'paper dois', 'file_name', 'language'])
        repository_name = ''
        count=0
        repos=[]
        for i in csv_dict_reader:
            doi = i['doi']
            title=i['title']
            paper_doi=i['paper_doi']
            file_name=i['file_name']
            flag = False
            if read_data(file_name):
                print(file_name)
                print(paper_doi)
                writer.writerow([doi, title, paper_doi, file_name, 'python'])
                count=count+1
            print('------')
            
        print(count)
        print(repos)
    
def download_files_from_dryad(doi):
    print('doi', doi)
    link = 'https://datadryad.org'+doi
    r = requests.get(link, params={'access_token': ACCESS_TOKEN}).json()
    print(r['_links'])
    if 'stash:download' in r['_links']:
        download_link='https://datadryad.org'+r['_links']['stash:download']['href']
        print('download link', download_link)
        wget.download(download_link, out="D:\knowledge extraction\dryadsoftware")

def download_selected_files():
    with open('softwareData.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        repository_name = ''
        count=0
        repos=[]
        for i in csv_dict_reader:
            repository_name = i['repository_name']
            head, tail = os.path.split(i['zenodo_url'])
            flag = False
            languages = ast.literal_eval(i['languages']) if i['languages'] != '' else ''
            if i['paper_doi'] != '' and repository_name not in repos:
                if i['paper_doi'][0] == '[':
                    paper_dois = ast.literal_eval(i['paper_doi'])
                    for pdoi in paper_dois:
                        if 'zenodo' not in pdoi and 'PANGAEA' not in pdoi and 'dryad' not in pdoi and 'figshare' not in pdoi and (
                                'python' in languages or 'Python' in languages):
                            flag = True
                        else:
                            paper_dois = [i['paper_doi']]
                            if 'zenodo' not in paper_dois and 'PANGAEA' not in paper_dois and 'dryad' not in paper_dois and 'figshare' not in paper_dois and (
                                    'python' in languages or 'Python' in languages):
                                flag = True
                        if flag and repository_name not in repos:
                            folder = ''
                            #file = 'D:\\knowledge extraction\\downloadedFiles/' + repository_name
                            #print(file)
                            if not is_file_exist("downloadedFiles/" + tail):
                                count=count+1
                                repos.append(tail)
                                print(tail)
                                #resp = requests.get(i['zenodo_url'],params={'access_token': ACCESS_TOKEN})
                                #print(resp)
                                #print(count)
                                #print(i['zenodo_url'])
                                #head, tail = os.path.split(i['zenodo_url'])
                                ##zname = "D:\\knowledge extraction\\downloadedFiles/"+tail
                                #zname = "downloadedFiles/"+tail
                                #zfile = open(zname, 'wb')
                                #zfile.write(resp.content)
                                #zfile.close()
                            else:
                                print('file already exist')
                                #count=count+1
                                #print(count)
        print(count)
        #print(repos)


def download_zenodo_repositories():
    with open('softwareData.csv', 'r', encoding="utf-8") as csv_file:
        csv_dict_reader = DictReader(csv_file)
        count=0
        for i in csv_dict_reader:
            url=i['zenodo_url']
            head, tail = os.path.split(url)
            print(url)
            if not is_file_exist("downloadedFiles/"+tail):
                resp = requests.get(url,params={'access_token': ACCESS_TOKEN})
                print('count', count)
                print(resp)
                    
                zname = "downloadedFiles/"+tail
                zfile = open(zname, 'wb')
                zfile.write(resp.content)
                zfile.close()
                #time.sleep(35)
            else:
                print('file already exist')
            count=count+1

def get_software_metadata_from_dryad():
    with open('dryadData.csv', 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        count=0
        request_link='https://datadryad.org/api/v2/datasets?q=software'
        while len(request_link) >0:
            r = requests.get(request_link,params={'Authorization' : "Bearer"+ ACCESS_TOKEN})
            r.status_code
            data=r.json()
            size=0
            datasets=data['_embedded']['stash:datasets']
            for s in datasets:
                if 'storageSize' in s:
                    size = s['storageSize']
                if  size<=400000000:
                    print(size)
                    count=count+1
                    print('count:' ,count)
                    doi=s['identifier']
                    print(doi)
                    self_link = s['_links']['self']['href']
                    download_files_from_dryad(self_link)
                    title=s['title']
                    description=s['abstract']
                    if 'relatedWorks' in s:
                        for i in s['relatedWorks']:
                            print(i['identifier'], i['identifierType'])
                        #writer.writerow([i['doi'], key, meta, url])
            if 'next' in data['_links']:
                request_link = 'https://datadryad.org'+data['_links']['next']['href']
                print('request_link\n', request_link)
            else:
                request_link = ''
    print(count)
    csv_file.close()
    
def download_files_from_figshare(link):
    print('software link', link)
    r=''
    while r == '':
        try:
            r = requests.get(link)
            break
        except:
            print("Connection refused by the server")
            time.sleep(10)
            continue
    #r = requests.get(link, headers={'Authorization': 'b30efcf1ff2f5371123308a229ee5900411ea42fce44f6af81478f3e0ee27fa4d070514ad2da31f3f144a840dd90661431c840304cd013b94d73087d0abad865'}).json()
    r=r.json()
    size=0
    file_name=''
    download_url=''
    #if len(r['files'])>=0:
    if 'files' in r and len(r['files'])>0:
        size=r['files'][0]['size']
        file_name=r['files'][0]['name']
        download_url=r['files'][0]['download_url']
    return { 'size': size, 'file_name': file_name, 'download_url': download_url }
    
def get_software_metadata_from_figshare():
    page=1
    with open('figshareData.csv', 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        page=91
        request_link='https://api.figshare.com/v2/articles?page='+str(page)+'&page_size=90&item_type=9'
        r = requests.get(request_link, verify=False)
        data=r.json()
        size=0
        count=1
        element=-1
        while len(data)>0:
            print(request_link)
            for s in data:
                if count>element:
                    print('count:' ,count)
                    count=count+1
                    result = download_files_from_figshare(s['url_public_api'])
                    if  (result['size']>0 and result['size']<=2147483648) and (result['file_name'].endswith('.zip') or result['file_name'].endswith('.ZIP')):
                        print('size', result['size'])
                        doi = s['doi']
                        title = s['title']
                        paper_doi = s['resource_doi']
                        print(result['file_name'])
                        resp=''
                        if result['download_url']!='' and not is_file_exist("D:\knowledge extraction\figsharesoftware/" + result['file_name']):
                            print(result['download_url'])
                            #wget.download(result['download_url'], out="D:\knowledge extraction\figsharesoftware")
                            while resp == '':
                                try:
                                    resp = requests.get(result['download_url'])
                                    break
                                except:
                                    print("Connection refused by the server..")
                                    time.sleep(10)
                                    continue
                            #resp = requests.get(result['download_url'],headers={'Authorization': '171f0d900adf8374172f041ed0227e659cf11360e3e856295377afac25df717f686abdd137bcc15994eb3aab3dd569e58f82c82c4b09bb1d08f1de55af6279d9'})
                            print(resp)
                            #head, tail = os.path.split(i['zenodo_url'])
                            #zname = "D:\\knowledge extraction\\figsharesoftware/"+result['file_name']
                            try:
                                zname = "figsharesoftware/"+result['file_name']
                                zfile = open(zname, 'wb')
                                zfile.write(resp.content)
                                zfile.close()
                            except:
                                print('error')
                        print('doi', doi)
                        print('title', title)
                        print('paper doi', paper_doi)
                        print('file name', result['file_name'])
                        writer.writerow([doi, title, paper_doi, result['file_name']])
                        print('------')
                else:
                    count=count+1
            page=page+1
            request_link='https://api.figshare.com/v2/articles?page='+str(page)+'&page_size=90&item_type=9'
            data = requests.get(request_link).json()
            count=1
            element=0
    print(count)
    csv_file.close()
    
    
def count_papers():
    with open('figsharesoftwarepackages.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        repository_name = ''
        count=0
        repos=[]
        for i in csv_dict_reader:
            #doi = i['doi']
            title=i['title']
            paper_doi=i['paper_doi']
            file_name=i['file_name']
            flag = False
            if paper_doi!='':
            #if read_data(file_name):
            #    print(file_name)
            #    print(paper_doi)
            #    writer.writerow([doi, title, paper_doi, file_name, 'python'])
                count=count+1
            print('------')
            
        print(count)
        print(repos)

def main():
    #count_papers()
    get_software_metadata_from_figshare()
    #filter_python_figshare_packages()
    #parse_figshare_python_packages()
    #download_zenodo_repositories()
    #download_selected_files()
    #get_python_R_packages()
    #download_python_files()


if __name__ == "__main__":
    main()
    

