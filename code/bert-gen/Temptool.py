filedir = input("input the location of file you want to pre-process:")

writefile = input("input the folder you want to put txt into:")
name = input("name your txt file:")

txtname = writefile+r"/"+name+".txt"

cnt = 0

with open(filedir,'r+',encoding = 'utf-8') as f:
    arr = f.readlines()
    for line in arr:
        line = line.replace('\n','')
        string = line+"||,||"+str(cnt)+'\n'
        
        with open(txtname,'a',encoding='utf-8') as txtfile:
            txtfile.write(string)
        
        cnt += 1
