from csv import DictReader
import ast
import os
import re
import json
import time
import csv
from csv import writer
import requests
from orkg import ORKG
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD
from shortid import ShortId
import pandas as pd

api = 'http://localhost:8080'
api_resources = '{}/api/resources/'.format(api)
api_predicates = '{}/api/predicates/'.format(api)
api_literals = '{}/api/literals/'.format(api)
api_statements = '{}/api/statements/'.format(api)
api_classes = '{}/api/classes/'.format(api)
orkg = ORKG(host=api)

def create_or_find_predicate(label):
    found = orkg.predicates.get(q=label, exact=True).content
    if len(found) > 0:
        predicate = found[0]['id']
    else:
        predicate = orkg.predicates.add(label=label).content['id']
    return predicate


def create_or_find_resource(label):
    found = orkg.resources.get(q=label, exact=True).content
    if len(found) > 0:
        resource = found[0]['id']
    else:
        resource = orkg.resources.add(label=label).content['id']
    return resource

def add_paper_in_orkg(doi, software_id):
    hasImplementationPredicate = create_or_find_predicate(label='Has implementation')
    paper = {
        "paper": {
            "doi": doi,
            "researchField": "R135",  # Databases/Information Systems
            "contributions": [
                {
                    "name": "Contribution 1",
                    "values": {
                        "P32": [
                            {"@id": nameAmbiguityProblem}
                        ],
                        hasImplementationPredicate: [
                            {"@id": software_id}
                        ],
                        similarityPredicate: [
                            {"@id": createOrFindResource('Cosine')},
                            {"@id": createOrFindResource(
                                'Eigen Decomposition')}
                        ],
                        usedMethodPredicate: [
                            {"@id": createOrFindResource(
                                'Boosted tree classification')}
                        ],
                        performanceMetricPredicate: [
                            {"@id": createOrFindResource('Precision')},
                            {"@id": createOrFindResource('Recall')},
                            {"@id": createOrFindResource(
                                'Misclassification error rate')}
                        ],
                        uncertaintyPredicate: [
                            {"text": "F"}
                        ],
                        datasetPredicate: [
                            {"text": "Not standard"}
                        ],
                        evidencePredicate: [
                            {"@id": createOrFindResource('Author name')},
                            {"@id": createOrFindResource('Venues')},
                            {"@id": createOrFindResource('Keywords')},
                            {"@id": createOrFindResource('Title words')},
                            {"@id": createOrFindResource('Abstract')},
                            {"@id": createOrFindResource('Subject category')}
                        ],
                        capabilityPredicate: [
                            {"@id": homonymsProblem}
                        ],
                        limitationsPredicate: [
                            {"text": "How to decide the splitting point and how to control the size of the tree."}
                        ]
                    }
                }
            ]
        }
    }

    paper = doiLookup(paper)
    response = orkg.papers.add(paper)
    
   
def add_related_paper(dois):
    print(dois)
    for doi in dois:
        print(doi)
    
    
    
    
def add_software(doi, name, url, languages, title, previousVersion, reference_urls, description, ref_dois):
    descriptionPredicate = create_or_find_predicate(label='description')
    ToolsLanguagesPredicate = create_or_find_predicate(label='Tools & Languages')
    UrlPredicate = create_or_find_predicate(label='Url')
    HasReferencePredicate = create_or_find_predicate(label='Has reference')
    HasPreviousVersionPredicate = create_or_find_predicate(label='Has Previous Version')
    print('adding software in orkg')
    languageList=[]
    [languageList.append({"text": l}) for l in languages]
    
    urlList=[]
    papersDoi=[]
    for j in ref_dois:
        if 'zenodo' in j or 'figshare' in j or 'dryad' in j:
            urlList.append({"text": j})
        else:
            papersDoi.append(j)
    
    
    [urlList.append({"text": refurl}) for refurl in reference_urls]
    
        #response = orkg.papers.add(p)
        #response=orkg.papers.add(params=p, merge_if_exists=True)

        #print(response.content)
    software = {
            "predicates": [],
            "resource": {
                "name": name,
                "classes": [
                "Software"
            ],
            "values" : {
            descriptionPredicate: [
                {
                    "text": description
                }
            ],
            ToolsLanguagesPredicate: languageList,
            UrlPredicate: [
                {
                    "text": url
                }
            ],
            "P26": [
                {
                    "text": doi
                }
            ],
            HasReferencePredicate: urlList,
            HasPreviousVersionPredicate : [
                {
                    "text": previousVersion
                }
            ]
        }
    }
    }
        #"title": data_list[i]['title'],
        #"authors": data_list[i]['authors'],
        #"publicationYear": data_list[i]['year'],
        #"doi": data_list[i]['doi'],
        #"researchField": "R57",
            #}  
        #}
    #response=orkg.objects.add(params=software).content
    print('url', urlList)
    if(len(papersDoi)>0):
        add_related_paper(papersDoi)
    #print(response.id)


def remove_special_characters(s):
    special_characters = ['!', '#', '$', '%', '&',  '@', '[', ']', ' ', '{', '}', '"', ',', '*', ')', '(']
    a2 = ''
    for i in s:
        if(i not in special_characters):
            a2 = a2 + i
    if a2[len(a2)-1] in '.' or a2[len(a2)-1] in '/':
        a2=a2[:-1]
    return a2

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
    
def arrange_dois(dois):
    doiList=[]
    for doi in dois:
        exp=re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        r= exp.search(doi)
        if r!=None:
            exp=re.compile(r"(10\.\d{1,50}/\S+)")
            rn= exp.search(r.group(1))
            if rn!=None:
                doiList.append(rn.group(1))
        else:
            doiList.append(doi)
    return doiList

def get_software_versions():
    versionsList={}
    with open('data.csv', 'r', encoding="utf-8") as my_file1:
     #passing file object to DictReader()
        csv_dict_reader = DictReader(my_file1)
        for it in csv_dict_reader:
            if it['identifier']!='':
                identifier=ast.literal_eval(it['identifier'])
            #print the values
                doi=''
                for info in identifier:
                    if info['relation']=='isVersionOf' and info['scheme']=='doi':
                        #versionsList[it['doi']] = {}
                        versionsList[it['doi']] = info['identifier']
    return versionsList           

def read_software_data():
    #open the file
    versionsList=get_software_versions()
    with open('softwareData.csv', 'r', encoding="ISO-8859-1") as my_file:
     #passing file object to DictReader()
        csv_dict_reader = DictReader(my_file)
     #iterating over each row
        for i in csv_dict_reader:
            doi=i['doi']
            print(doi)
            name=i['name'] if i['name']!='' else ''
            url=i['url']
            languages=ast.literal_eval(i['languages']) if i['languages']!='' else '' #
            title=i['title'] if i['title']!='' else ''
            previousVersion=versionsList[doi] if doi in versionsList else ''
            reference_urls=ast.literal_eval(i['ref_url']) if i['ref_url']!='' else '' #
            paper_dois=[]
            if i['paper_doi']!='':
                if i['paper_doi'][0]=='[':
                    paper_dois=ast.literal_eval(i['paper_doi'])
                else:
                    paper_dois=[i['paper_doi']]
            description=i['description'] if i['description']!='' else ''
            ref_dois=[]
            if len(paper_dois)>0:
                ref_dois=arrange_dois(paper_dois)
            add_software(doi, name, url, languages, title, previousVersion, reference_urls, description, ref_dois)
            print(doi, name, url, languages, title, previousVersion, reference_urls, description, ref_dois)
            print("\n")
                        #doi, repository name, description, url, title, languages, paper_doi, paper_reference, paper_title
    
            
            
def main():
    read_software_data()


if __name__ == "__main__":
    main()
