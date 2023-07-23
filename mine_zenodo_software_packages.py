import requests
import os.path
from zipfile import ZipFile
import time
from pathlib import Path
import csv
from csv import writer
from csv import DictReader
import ast
import wget
import urllib.parse

def is_file_exist(filePath):
    my_file = Path(filePath)
    if my_file.is_file():
        return True
    else:
        return False

ACCESS_TOKEN = 'pAnsWkTqE24YWG1p2cNveBBLfvif0Wsk4JpSAWj467mApZcg59O7meOKAbQt'

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
{'s': '2022-09-02', 'e': '2023-01-01'},
{'s': '2023-01-02', 'e': '2023-05-01'},
{'s': '2023-05-02', 'e': '2023-09-01'}]
    


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
    my_file=open('softwareData.csv', 'r', encoding="ISO-8859-1")
    csv_dict_reader = DictReader(my_file)
    count = 0
    visited_doi = []
    for i in csv_dict_reader:
        #print(i['doi'])
        flag = False
        languages=''
        repository_name = i['repository_name']
        head, tail = os.path.split(i['repo_url'])
        #print(repository_name)
        languages=i['languages']
        if languages!='':
            languages=ast.literal_eval(languages)
            
            
        if 'Python' in languages or 'python' in languages or 'Jupyter Notebook' in languages: 
            paper_dois = ast.literal_eval(i['paper_doi'])
            for doi in paper_dois:
                if is_paper_doi(doi) and doi not in visited_doi:
                    #print(doi)
                    count = count+1
                    visited_doi.append(doi)
                    print(doi)
                    flag = True
                #uncoment when to download the data
            '''    
            if flag and not is_file_exist("downloadedFiles/" + tail):
                print(i['repo_url'])
                print(count)
                resp = requests.get(i['repo_url'],params={'access_token': ACCESS_TOKEN})
                print('count', count)
                print(resp)
                    
                zname = "D:\knowledge extraction\downloadedFiles/"+tail
                zfile = open(zname, 'wb')
                zfile.write(resp.content)
                zfile.close()
                #wget.download(repo_url, out="D:\knowledge extraction\downloadedFiles")
            else:
                print('file already exist')
            '''       
                    
    print(count)

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

def get_software_metadata_from_zenodo():
    with open('zenodo_data.csv', 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for date in date_ranges:
            time.sleep(100)
            request_link='https://zenodo.org/api/records/?q=created:%5B'+date['s']+'%20TO%20'+date['e']+'%5D&type=software&size=9999'
            print(request_link)
            r = requests.get(request_link,params={'access_token': ACCESS_TOKEN})
            r.status_code
            data=r.json()
            aggregations=data['aggregations']['type']['buckets']
            value=[element for element in aggregations if element['key'] == 'software']
            if len(value) > 0:
                print('software', value[0]['doc_count'])
            repositories=data['hits']['hits']
            print('repo', len(repositories))
            count=0
            print('count:' ,count)
            for i in repositories:
                url = ''
                size = 0
                key = ''
                if 'files' in i and len(i['files'])>0:
                    if 'links' in i['files'][0]:
                        url = i['files'][0]['links']['self']
                        size = i['files'][0]['size']
                        key = i['files'][0]['key']
                    #if size<400000000:
                    if size<=2147483648:
                        if os.path.splitext(url)[1]=='.zip' or os.path.splitext(url)[1]=='.ZIP':
                            print(url, size)
                            meta=''
                            head, tail = os.path.split(url)
                            if 'doi' in i:
                                print('doi',i['doi'])
                            if 'metadata' in i: #and 'related_identifiers' in i['metadata']:
                                print('metadata')
                                if 'related_identifiers' in i['metadata']:
                                    meta=i['metadata']['related_identifiers']
                                    print(i['metadata']['related_identifiers'])
                            writer.writerow([i['doi'], key, meta, url])
    csv_file.close()

def main():
    #get_software_metadata_from_zenodo()
    #download_zenodo_repositories()
    #download_selected_files()
    #get_python_R_packages()
    download_python_files()


if __name__ == "__main__":
    main()
    

