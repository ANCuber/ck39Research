from latexprocessing import givenoise
filedir = input("input file dir")

writedir = input("write dir")

with open(filedir,'r',encoding="utf-8") as reader:
    lines= reader.readlines()
    for line in lines:
        with open(writedir,'a',encoding="utf-8") as writer:
            towrite=("".join(givenoise(line))).strip('\n')+"";
            towrite+="||,||"
            towrite += ""+("".join(line.strip('\n')))+"\n"
            print(line)
            print(towrite)
            writer.write(towrite)