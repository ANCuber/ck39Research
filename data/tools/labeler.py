import matplotlib.pyplot as plt

filedir = input("input the location of file you want to label:")
writefiledir = input("input the location of file you want to write to:")
plt.ion()
plt.show()
curlinen = 0
try:
    with open(writefiledir,'r',encoding='utf-8') as rl:
        arr = rl.readlines()
        curlinen = int((arr[-1])[3:-3])
    print("starting at line {}".format(curlinen))
except:
    print("create new file at:"+writefiledir)
with open(filedir,'r',encoding='utf-8') as f:
    arr = f.readlines()
    for i in range(curlinen,(len(arr))):
        line = arr[i]
        line = line.strip('\n')
        print(line)
        a = line
        ax = plt.subplot(111)
        ax.clear()
        try:
            ax.text(0,0.5,r"$%s$" %(a),fontsize=30,color="green")
            des = input("input description:");
        except:
            print("there is an error in LaTex commands")
            continue;
        if(des=="skip"):
            continue
        if(des=='exit' or des=='quit'):
            with open(writefiledir,'a',encoding='utf-8') as bw:
                bw.writelines("---{}--\n".format(i-1))
            exit()
        with open(writefiledir,'a',encoding='utf-8') as w:
            w.writelines(a+"||,||"+des+"\n");