from latexprocessing import givenoise
filedir = input("input file dir")

writedir = input("write dir")

with open(filedir,'r',encoding="utf-8") as reader:
    lines= reader.readlines()
    for line in lines:
        with open(writedir,'a',encoding="utf-8") as writer:
            writer.write(lines+","+"".join(givenoise(lines))+"\n")