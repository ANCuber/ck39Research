from processing_func import *

filedir = input("input the location of file you want to pre-process:")
writefile = input("input the folder you want to write to:")

name = input("name your file:")

resultfile = writefile+r"/"+name+".txt"
t = 0

with open(filedir,'r',encoding = 'utf-8') as f:
    sour = f.readlines()
    totalsize = len(sour)
    percent = 0
    with open(resultfile, 'a') as res:
        for line in sour:
            t+=1
            print(ReplaceVariable(ReplacePunctuation(WrapLatexVar(line)).replace("[Pspa]","")), end = '', file = res)
            if(t>=(0.01*percent*totalsize)):
                print(percent,r"% done")
                percent+=1
        
