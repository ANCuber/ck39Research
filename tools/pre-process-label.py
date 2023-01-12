from processing_func import *

filedir = input("input the location of file you want to pre-process:")
writefile = input("input the folder you want to write to:")

name = input("name your file:")

resultfile = writefile+r"/"+name+".txt"

with open(filedir,'r',encoding = 'utf-8') as f:
    sour = f.readlines()
    for line in sour:
        pairdata = line.split('||,||')
        if(len(pairdata)!=2):
            continue
        pairdata[1] = pairdata[1].strip('\n')
        process = [ReplaceVariable(ReplacePunctuation(pairdata[0])),ReplaceVariableDes(WrapLatexVar(pairdata[1])).replace('{','').replace('}','').replace(' ','[Pspa]')]
        with open(resultfile,'a') as res:
            print(process[0],"||,||",process[1],end='\n',file=res)

        
