# -*- coding: utf-8 -*-
#-m !pip3 install rank_bm25
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("/home/12518research/ck39Research/model/bert-p2000&chi")
from rank_bm25 import BM25Okapi
import csv

doc_dir = "/home/12518research/ck39Research/data/Data/bm25/newdata.csv"
#dataset for retrieving
with open(doc_dir,'r') as file:
    corpus = csv.reader(file)
    tokencorpus = []
    latex = []
    #print(len(latex))
    for line in corpus:
        line[0]= line[0].strip(' ')
        line[1] = line[1].strip(' ')
        tokencorpus.append(tokenizer.tokenize(line[1]))
        latex.append(line[0])
    bm25 = BM25Okapi(tokencorpus)

def listtoword(arr):
    s = ""
    for i in arr:
        s+=i
    s = s.replace(' ','')
    return s



def retrieve(query,top_k):
    #for loop start here
    tokenized_query = tokenizer.tokenize(query)
    #print(tokenized_query)
    score = bm25.get_scores(tokenized_query)
    score = score.tolist()

    x = []
    x.extend(score)
    x.sort(reverse=True)
    a = x[:top_k]
    res = []
    for i in a:
        res.append(score.index(i))
        
    ret = '[CLS]'+query+'[SEP]'

    for i in res:
        output = '[CLS]'+listtoword(latex[i]).strip('\|\|')+'[SEP]'+listtoword(tokencorpus[i]).strip('\|\|')+'[SEP]'
        ret = ret+output
            
    return ret


def mainfunc():
    convertdir = ""
    #process training data for generator
    raw_data = input("input the file you want to process:")
    writefile = input("input the folder you want to write to:")
    filename = input("name your file:")

    csvname = writefile+r"/"+filename+".csv"

    cnt = 0
    add = 50000
    ending = '[var50]'
    
    with open(raw_data,'r',encoding = 'utf-8') as f:

        #with open(csvname,'w',newline='') as csvfile:
            #writer = csv.writer(csvfile, delimiter=',')
        #writer.writerow(['retrieved','target','id'])
        with open(csvname,'a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            lines = f.readlines()
            for line in lines:
                cnt += 1
                if line[0:3] == "---" or line[0:3] == "tar":
                    continue
                line = line.split('||,||')
        
                line[1] = line[1].replace('\n','')
                line[1] = line[1].replace(' ','')

                result = retrieve(line[1],top_k=5)

                tar = line[0].replace(' ','')
                tar = tar.replace('#','')
                writer.writerow([result,'[CLS]'+tar+ending+'[SEP]',str(cnt)])