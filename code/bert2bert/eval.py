# -*- coding: utf-8 -*-
#-m !pip3 install rank_bm25
from transformers import AutoTokenizer
import os
cwd = os.getcwd()
tokenizer = AutoTokenizer.from_pretrained(cwd+"/model/bert-p2000&chi")
from rank_bm25 import BM25Okapi
import csv
arr = [0]*1000
doc_dir = cwd+"/result.csv"

cnt = 0
base = 0

#dataset for retrieving
with open(doc_dir,'r') as file:
    corpus = csv.reader(file)
    
    #print(len(latex))
    for line in corpus:
        
        line[0]= line[0].strip(' ')
        
        line[1] = line[1].strip(' ')
    

        list_0 = tokenizer.tokenize(line[0])
        list_1 = tokenizer.tokenize(line[1])

        base += len(list_0)
        i = 0
        closecnt = 0
        for j in range(len(list_1)):
            if i >= len(list_0):
                break
            while list_0[i] != list_1[j] and i < len(list_0)-1:
                i += 1
            i += 1
            cnt += 1
            closecnt+=1
        
print(cnt)
print(base)
print(cnt/base)