from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
response = requests.get(
	url="https://en.wikipedia.org/wiki/Quadratic_equation",
)
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
            with open("database.txt", "a",encoding='utf-8') as file_object:
                file_object.write(postext)


