import csv

filedir = input("input the file you want to convert(.txt):")
writefile = input("input the folder you want to put csv into:")
name = input("name your csv file:")

csvname = writefile+r"/"+name+".csv"
with open(filedir,'r',encoding = 'utf-8') as f:
    arr = f.readlines()
    for line in arr:
        if(line[0:3]=="---"):
            continue
        pairstuff = line.split("||,||")
        with open(csvname,'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(pairstuff)