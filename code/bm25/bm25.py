#!pip3 install rank_bm25
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("/home/12518research/ck39Research/code/Pretrain/model")

from rank_bm25 import BM25Okapi

import csv
def listtoword(arr):
    s = ""
    for i in arr:
        s+=i
    s = s.replace(' ','')
    return s




doc_dir = "/home/12518research/ck39Research/data/Data/dpr/1000data1/newdata.csv"
with open(doc_dir,'r') as file:
    corpus = csv.reader(file)
    tokencorpus = []
    latex = []
    print(len(latex))
    for line in corpus:
        line[0]= line[0].strip(' ')
        line[1] = line[1].strip(' ')
        tokencorpus.append(tokenizer.tokenize(line[1]))
        latex.append(line[0])
    bm25 = BM25Okapi(tokencorpus)

    #for loop start here
    query = "cos[Pspa][var1]的[var2]次方[Pspa]分之12"
    tokenized_query = tokenizer.tokenize(query)
    print(tokenized_query)
    score = bm25.get_scores(tokenized_query)
    score = score.tolist()
    top_k = 5

    x = []
    x.extend(score)
    x.sort(reverse=True)
    a = x[:top_k]
    res = []
    for i in a:
        res.append(score.index(i))
    for i in res:
        print(listtoword(latex[i]),listtoword(tokencorpus[i]),end='\n\n')