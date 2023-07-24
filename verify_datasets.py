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
import pdfplumber
from difflib import SequenceMatcher
from python_keywords import is_python_keyword
from tika import parser
import fitz
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
from nltk.util import ngrams
from nltk import word_tokenize
embedder = SentenceTransformer('all-MiniLM-L6-v2')

global_count=0
oa=0
ca=0

def remove_special_characters(s):
    special_characters = ['!', '#', '$', '%', '&',  '@', '[', ']', ' ', '{', '}', '"', ',', '*', ')', '(', ':', """'""", '`', ';']
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


def is_file_exist(doi):
    global global_count
    filePath='paper-pdfs/'+doi.replace('/', '')+'.pdf'
    my_file = Path(filePath)
    if my_file.is_file():
        #print('exist')
        global_count=global_count+1
        #print(global_count)
        return True
    else:
        return False
    
def get_file_extension(file_name):
    name, extension=os.path.splitext(file_name)
    return extension

def is_paper_doi(doi):
    if 'zenodo' not in doi and 'PANGAEA' not in doi and 'dryad' not in doi and 'figshare' not in doi and 'arXiv' not in doi:  
        return True
    return False
    
def break_string(s):
    result = re.split('<|>|\\?', s)
    return result[0]
    
def refine_doi_string(doi):
    ref=get_reference_url(doi)
    if len(ref)>0:
        #ref_doi=get_paper_doi(ref[0])
        split_res=doi.split("http")
        if len(split_res)>0:
            doi=split_res[0]
        
    doi=remove_special_characters(doi)
    doi=break_string(doi)
    return remove_special_characters(doi)

def get_paper_doi(reference):
    exp=re.compile(r"(10\.\d{1,50}/\S+)")
    doi= exp.findall(reference)
    res=''
    if doi !=None:
        i=0
        while(i<len(doi)):
            doi[i]=remove_special_characters(doi[i])
            i=i+1
        res=list(set(doi))
    else:
        res= ''
    return res
    
def get_reference_url(reference):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, reference)
    res=''
    urls=[]
    temp=''
    if links !=None:
        for lnk in links:
            temp = lnk[0]
            if (temp[len(temp)-1] in ')' and temp[len(temp)-1] in ',') or (temp[len(temp)-1] in ',' and temp[len(temp)-1] in ')') :
                temp=temp[:-1]
            if temp[len(temp)-1] in ')' or temp[len(temp)-1] in ',':
                temp=temp[:-1]
            urls.append(temp)
        res=list(set(urls))
    else:
        res= ''
    return res
        
def organize_data(sk, terms):
    sk_data={}
    sk_data['input_files']=[]
    sk_data['operations']=[]
    sk_data['output_files']=[]
    for key in terms.keys():
        for entry in terms[key]:
            if entry in sk:
                sk_data[key].append(entry)
                
    print(sk_data)
    return sk_data

def clean_sentence(sentence):
    sentence = sentence.lower().strip()
    sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
    return re.sub(r'\s{2,}', ' ', sentence)

def tokenize(sentence):
    return [token for token in sentence.split() if token not in STOP_WORDS and len(token)>2 and not token.isdigit()]

def create_corpus_embeddings(corpus):
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    return corpus_embeddings

def search_string_in_text(string, corpus_embeddings, corpus):
# Corpus with example sentences
    #corpus = pdf_words
    #corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

# Query sentences:
    queries = string #['A man is eating pasta.', 'Someone in a gorilla costume is playing a set of drums.', 'A cheetah chases prey on across a field.']


# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = min(2, len(corpus))
    result=[]
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        for score, idx in zip(top_results[0], top_results[1]):
            if score>=0.52 and query not in result:
                result.append(query)
    result=list(set(result))
    return result

def form_string(array):
    string=[]
    for s in array:
        new_str=''
        temp = re.sub("([a-z])([A-Z])","\g<1> \g<2>",s)
        temp=re.split('[_.]', temp)
        for t in temp:
            t=t.lower()
            if not is_python_keyword(t) and len(t)>2:
                new_str=new_str+' '+t
        if len(new_str) > 0:
            new_str=new_str.strip()
            string.append(new_str)

    string=list(set(string))
    return string


def search_terms_in_pdf(pdf_words, pdf_words_embeddings, terms):

    sk_data={}
    sk_data['input_files']=[]
    sk_data['operations']=[]
    sk_data['output_files']=[]

    input_files=list(set(terms['input_files']))
    for file in input_files:
        response=form_string(input_files)
        if len(response)>0 and len(pdf_words_embeddings)>0:
            result=search_string_in_text(response, pdf_words_embeddings, pdf_words)
            if len(result)>0:
                sk_data['input_files'].append(file)   


    response=form_string(terms['operations'])
    if len(response)>0 and len(pdf_words_embeddings)>0:
        result=search_string_in_text(response, pdf_words_embeddings, pdf_words)
        for r in result:
            if not is_python_keyword(r):
                sk_data['operations'].append(r)

    output_files=list(set(terms['output_files']))
    for file in output_files:
        response=form_string(output_files)
        if len(response)>0 and len(pdf_words_embeddings)>0:
            result=search_string_in_text(response, pdf_words_embeddings, pdf_words)
            if len(result)>0:
                sk_data['output_files'].append(file)    


    #sk=list(set(lst))
    print('result')
    print(sk_data)
    return sk_data
    #return organize_data(sk, terms)

def parse_data_from_pdf(doi):
    print(doi)
    filePath='paper-pdfs/'+doi.replace('/', '')+'.pdf'

    doc=''
    try:
        doc = fitz.open(filePath)
    except:
        print('pdf error')

    string = []

    text=''
    for page in doc:
        #print(page)
        text=text+' '+page.get_text().lower()

    text1=text.replace('\n', ' ')#.replace("?","").replace(".","")

    original_text=clean_sentence(text1)
    text=tokenize(original_text)
    bigram = list(ngrams(text, 2)) 
    
    pdf_words=[]
    for r in bigram:
        pdf_words.append(r[0]+' '+r[1])
    trigram = list(ngrams(text, 3))

    for r in trigram:
        pdf_words.append(r[0]+' '+r[1]+' '+r[2])
    pdf_words=list(set(pdf_words)) 

    return pdf_words


def get_request(url):
    rpdf=''
    count=0
    while rpdf == '':
        try:
            rpdf = requests.get(url, stream=True)
            return rpdf
        except:
            count=count+1
            if count>5:
                return ''
            print("Connection refused by the server..")
            time.sleep(10)
            continue
    
def get_all_pdfs(doi):
    global oa
    global ca
    url = 'https://api.unpaywall.org/v2/'+doi+'?email=hariskmohammadk@gmail.com'
    print(url)
    pdf_urls=[]
    title=''
    r=''
    while r == '':
        try:
            r = requests.get(url).json()
            break
        except:
            print("Connection refused by the server..")
            time.sleep(10)
            continue
    
    if 'HTTP_status_code' in r:
        return ''
    if 'best_oa_location' in r and r['best_oa_location']!=None and 'url_for_pdf' in r['best_oa_location'] and r['best_oa_location']['url_for_pdf']!=None:
        pdf_urls.append(r['best_oa_location']['url_for_pdf'])
        title= r['title']

    if 'first_oa_location' in r and r['first_oa_location']!=None and 'url_for_pdf' in r['first_oa_location'] and r['first_oa_location']['url_for_pdf']!=None:
        pdf_urls.append(r['first_oa_location']['url_for_pdf'])
        title= r['title']

    if 'oa_locations' in r and r['oa_locations']!=None:
        for i in r['oa_locations']:
            if 'url_for_pdf' in i and i['url_for_pdf']!=None:
                pdf_urls.append(i['url_for_pdf'])
                title= r['title']
    
    if len(pdf_urls)>0:
        oa = oa+1
    else:
        ca = ca+1

    
    if len(pdf_urls)>0:
        print(pdf_urls)
        for pdf in pdf_urls:
            file = get_request(pdf)
            if file!='' and file.status_code==200:
                print("downloading")
                file_name='paper-pdfs/'+doi.replace('/', '')+'.pdf'
                f=open(file_name, 'wb')
                f.write(file.content)
                break
        #file_name='paper-pdfs/'+doi.replace('/', '')+'.pdf'
        #os.rename('paper-pdfs/temp.pdf', file_name)
    
    print('-----') 
    #return None
    
def search_scholarly_knowledge():
    #extracted_data=read_extracted_data()
    with open('softwareData.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        count = 0
        visited_doi = []
        for i in csv_dict_reader:
            languages=''
            sk_response=''
            flag = False
            print(i['doi'])
            #head, tail = os.path.split(i['repo_url'])
            if i['languages']!='':
                languages=ast.literal_eval(i['languages'])
            print(languages)
            
            if 'Python' in languages or 'python' in languages or 'ipynb' in languages or 'IPYNB' in languages:
                paper_dois = ast.literal_eval(i['paper_doi'])
                for doi in paper_dois:
                    #if is_file_exist(doi) and is_paper_doi(doi) and doi not in visited_doi:
                    for doi in paper_dois:
                        if is_paper_doi(doi) and doi not in visited_doi:
                            #print(doi)
                            count = count+1
                            visited_doi.append(doi)
                            print('doi', doi)
                            flag = True
                            doi=refine_doi_string(doi)
                            print('original doi', doi)
                            if not is_file_exist(doi):
                                get_all_pdfs(doi)
                            print("-------") 
                    
    print(count)
    print(oa)
    print(ca)
    
def is_file_exist_in_directory(path, file_name):
    folders=path.split('/')
    root=folders[0]+'/'+folders[1]
    print(root)
    for dirpath, dirnames, filenames in os.walk(root):
        head, tail = os.path.split(file_name)
        if tail in filenames:
            print(dirpath)
            print(tail)
            return True
    return False
    

#for file_name in list(set(data['input_files'])): 
#                extension=get_file_extension(file_name)
#                if extension !='' and file_name not in temp:
                    #print(file_name)
#                    temp.append(file_name)
                    #extracted_data[i['doi']] = data
#                    if is_file_exist_in_directory(i['file_name'], file_name):
#                        count=count+1


def extract_scholarly_knowledge(doi_list, extracted_data):
    write_file=open('scholarly_knowledge.csv', 'a', encoding="utf-8", newline='')
    writer = csv.writer(write_file)
    for key in doi_list.keys():
        for doi in doi_list[key]:
            response=parse_data_from_pdf(doi)
            if len(response)>0:
                corpus_embeddings=create_corpus_embeddings(response)
                print(key, doi)
                if key in extracted_data:
                    parsed_code=extracted_data[key]
                    for it in parsed_code:
                        print(it['ed'])
                        sk=search_terms_in_pdf(response, corpus_embeddings, it['ed'])
                        if sk!=None and len(sk)>0 and len(sk['input_files'])>0 and len(sk['operations'])>0:
                            print('writing file')
                            writer.writerow([key, doi, it['filename'], sk])
                        print('----')

def read_extracted_data():
    software_metadata=read_software_metadata()
    count=0
    temp=[]
    datasets_used=0
    extracted_data={}
    doi_list={}
    with open('astData.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        for i in csv_dict_reader:
            #data = ast.literal_eval(i['data'])
            software_doi=i['doi']
            if software_doi not in extracted_data.keys():
                extracted_data[software_doi]=[]
                #extracted_data[software_doi]['data']={}
            extracted_data[software_doi].append({'filename': i['file_name'], 'ed': ast.literal_eval(i['data'])})

            software_doi=i['doi']
            if software_doi not in doi_list.keys():
                if software_doi in software_metadata.keys():
                    doi_list[software_doi]=[]
                    dois=list(set(software_metadata[software_doi]['dois']))
                    for doi in dois:
                        if is_file_exist(doi):
                            doi_list[software_doi].append(doi)
                        #else:
                        #    get_all_pdfs(doi)    
    extract_scholarly_knowledge(doi_list, extracted_data)



def perfectEval(anonstring):
        if len(anonstring) == 0:
            return ''
        try:
            ev = ast.literal_eval(anonstring)
            return ev
        except:
            return [anonstring]

def validate_doi(doi):
    ref=get_reference_url(doi)
    #print(ref)
    if len(ref)>0:
        updoi=get_paper_doi(ref[0])
        if len(updoi)>0:
            return updoi[0]
    else:
        return doi


def read_software_metadata():
    extracted_data={}
    with open('softwareDataa.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        count = 0
        visited_doi = []
        for i in csv_dict_reader:
            doi_list=[]
            sk_response=''
            flag = False
            repository_name = i['repository_name']
            head, tail = os.path.split(i['zenodo_url'])
            languages = ast.literal_eval(i['languages']) if i['languages'] != '' else ''
            if 'Python' in languages or 'python' in languages:
                paper_doi=i['paper_doi']
                dois = perfectEval(paper_doi)
                if len(dois) > 0:
                    for doi in dois:
                        if is_paper_doi(doi):
                            doi=validate_doi(doi)
                            if doi !=None:
                                #print(doi)
                                doi_list.append(doi)
                                count=count+1
                    if len(doi_list) > 0:
                        extracted_data[i['doi']] = {'dois': doi_list}
    print(count)
    return extracted_data



def read_parsed_data():
    count=0
    temp=[]
    datasets_used=0
    extracted_data={}
    with open('astData.csv', 'r', encoding="ISO-8859-1") as my_file:
        csv_dict_reader = DictReader(my_file)
        for i in csv_dict_reader:
            data = ast.literal_eval(i['data'])
            
        
        

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
    #read_software_metadata()
    #read_extracted_data()
    search_scholarly_knowledge()
    #pdf_info = {'pdf_url':{"https://arxiv.org/pdf/1603.06212.pdf"}}
    #search_terms_in_pdf(pdf_info, '', ['KNeighborsClassifier'])
    #read_extracted_data()
    #is_file_exist_in_directory('temp/JuliaDynamics-RecurrenceAnalysis.jl-7a2acc8/benchmarks/benchmark_rqa.py', 'rossler.txt')
    #is_article_open_access()


if __name__ == "__main__":
    main()
