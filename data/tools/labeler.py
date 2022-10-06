import matplotlib.pyplot as plt

filedir = input("input the location of file you want to label:")
writefiledir = input("input the location of file you want to write to:")
plt.ion()
plt.show()
with open(filedir,'r',encoding='utf-8') as f:
    arr = f.readlines()
    for line in arr:
        line = line.strip('\n')
        print(line)
        a = line
        ax = plt.subplot(111)
        ax.text(0,0.5,r"$%s$" %(a),fontsize=30,color="green")
        des = input("input description:");
        ax.clear()
        with open(writefiledir,'a',encoding='utf-8') as w:
            w.writelines(a+","+des+"\n");