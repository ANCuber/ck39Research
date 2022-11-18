filedir = input("input the file you want to convert(.txt):")
writefile = input("input the folder you want to put txt into:")
name = input("name your txt file:")

txtname = writefile+r"/"+name+".txt"
with open(filedir,'r',encoding = 'utf-8') as f:
    arr = f.readlines()
    for line in arr:
        if (line[0:3] == "---"):
            continue
        s = line.split("||,||")
        with open(txtname,'a') as txtfile:
            txtfile.write(s[1])
