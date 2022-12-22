from html.parser import HTMLParser
from latexprocessing import norm
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
writefiledir = input("input file dir:")

while(True):
    url = input("input web address:")
    response = requests.get(
        url=url
    )

    soup = BeautifulSoup(response.content, 'html.parser')
    tags=soup.findAll('img')
    for tex in tags:
        postext = tex['alt']
        postext = norm(postext)
        if(len(postext)!=0):
            with open(writefiledir,'a',encoding='utf-8') as f:
                f.write(postext+'\n')
    print("complete! :)")
