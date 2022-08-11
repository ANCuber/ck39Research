from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
url = input("input web address:")
response = requests.get(
	url=url
)
writefiledir = "testdata_for_seq2seq_base.txt"
soup = BeautifulSoup(response.content, 'html.parser')
tags=soup.findAll('img')
for tex in tags:
    postext = tex['alt']
    if(len(postext)):
        if(postext.find('{')!=-1 or postext.find('\\')!=-1 or postext.find(',')!=-1): 
            postext = postext.replace("\\displaystyle","")
            postext = postext.replace("\\.","")
            postext=postext.replace(".","")
            postext = postext.replace("\\text","")
            postext = postext.replace("\\tfrac","\\frac")
            if(postext[-1]=='\\'):
                postext = postext[0:-2]
            if(postext[-1]==','):
                postext = postext[0:-2]
            postext= postext+'\n'
            with open(writefiledir, "a",encoding='utf-8') as file_object:
                file_object.write(postext)


