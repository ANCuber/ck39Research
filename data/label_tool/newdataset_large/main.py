import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
ax=plt.subplot(111)
with open('database.txt','r') as f:
    lines = f.readlines();
    for line in lines:
        ax=plt.subplot(111)
        a = r'{}'.format(line)
        #a = line
        a = a[:-1]
        print(a)
        ax.text(0, 0.5,'$%s$'%a,size=50,color='black')
        plt.show(block=False)
        g = input();
        with open('result.txt','a') as wf:
            wf.write(a+","+g+'\n');
            print(g + a)
            wf.close();
        plt.close()
#note: things to remove, \left \right \quad \space, redundent {} () , style