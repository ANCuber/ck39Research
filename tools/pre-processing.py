from processing_func import *

filedir = input("input the location of file you want to pre-process:")
writefile = input("input the folder you want to write to:")

name = input("name your file:")

resultfile = writefile+r"/"+name+".txt"

with open(filedir,'r',encoding = 'utf-8') as f:
    sour = f.readlines()
    for line in sour:
        with open(resultfile, 'a') as res:
            print(ReplaceVariable(ReplacePunctuation(line)), end = '', file = res)

        
