import random
# -*- coding:utf-8 -*-
def next_permutation(a):
    """Generate the lexicographically next permutation inplace.

    https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
    Return false if there is no next permutation.
    """
    # Find the largest index i such that a[i] < a[i + 1]. If no such
    # index exists, the permutation is the last permutation
    for i in reversed(range(len(a) - 1)):
        if a[i] < a[i + 1]:
            break  # found
    else:  # no break: not found
        return False  # no next permutation

    # Find the largest index j greater than i such that a[i] < a[j]
    j = next(j for j in reversed(range(i + 1, len(a))) if a[i] < a[j])

    # Swap the value of a[i] with that of a[j]
    a[i], a[j] = a[j], a[i]

    # Reverse sequence from a[i + 1] up to and including the final element a[n]
    a[i + 1:] = reversed(a[i + 1:])
    return True


filedir = input("input the location of file you want to agument")
writefile = input("input the folder you want to write to:")

name = input("name your file:")

resultfile = writefile+r"/"+name+".txt"
dataarr_per = []
with open(filedir,'r',encoding = 'utf-8') as f:
    sour = f.readlines()
    dataarr = [line.split('||,||') for line in sour]
    #var permutations:
    for pair in dataarr:
        pair[0] = pair[0].strip('\n')
        pair[1]=pair[1].strip('\n')
        pair[0] = pair[0].strip(' ')
        pair[1] = pair[1].strip(' ')
        pos = 1
        while(pair[0].find("[var{}]".format(pos))!=-1):
            pair[0]=pair[0].replace("[var{}]".format(pos),"--[var{}]--".format(pos))
            pair[1]=pair[1].replace("[var{}]".format(pos),"--[var{}]--".format(pos))
            pos+=1
        permutation = []
        for i in range(1,pos):
            permutation.append(i)
        k = True
        while(k):
            npair = []
            npair.append(pair[0])
            npair.append(pair[1])
            for i in range(1,pos):
                npair[0]=npair[0].replace("--[var{}]--".format(i),"[var{}]".format(permutation[i-1]))
                npair[1]=npair[1].replace("--[var{}]--".format(i),"[var{}]".format(permutation[i-1]))
            dataarr_per.append(npair)
            k = next_permutation(permutation)
    print(len(dataarr_per))

n = len(dataarr_per)

final = []
five_con_list = [["[Peql]","等於"],["[Ples]","小於"],["[Pbgr]","大於"],["[Pbeg]leq[Pspa]","小於等於"],["[Pbeg]geq[Pspa]","大於等於"]]
for i in dataarr_per:
    final.append(i)
for i in range(0,n):
    tobepair = random.sample(dataarr_per,(int)(0.01*n))
    for j in tobepair:
        a = dataarr_per[i][0]
        b = dataarr_per[i][1]
        c = j[0]
        d = j[1]
        k = random.randint(0,4);
        final.append([a+five_con_list[k][0]+c,b+five_con_list[k][1]+d])

print(len(final))

with open(resultfile,'a') as w:
    for pair in final:
        stri = pair[0]+"||,||"+pair[1]
        print(stri,file=w)
