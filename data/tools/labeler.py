

import matplotlib.pyplot as plt

filedir = input("input the location of file you want to label:")

with open(filedir,'r',encoding='utf-8') as f:
    arr = f.readlines()
    ax = plt.subplot(111)
    for line in arr:
        line = line.strip('\n')
        print(line)
        a = line
        ax.text(0.5,0.5,r"$%s$" %(a),fontsize=30,color="green")
        plt.show()