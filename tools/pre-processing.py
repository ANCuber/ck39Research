'''
* -> space and punctuation mark

common place holder:
 x,n,y,z,w,k,p,a,b,c,d

flow:
    replace variable
    replace punctuation
    replace numbers
'''
import re
def IsPuncutation(c):
    for h in punctuation_list:
        if(h==c):
            return 1
    return 0

variable_list = ["x","n","y","z","w","k","p","a","b","c","d","q","t","R","r"]
punctuation_list = ['[', ']',' ','^','+','-','(',')','/','{','}','\\','=','<','>',':','!','_']
punc_to_token = {"[":"[Plmb]","]":"[Prmb]"," ":"[Pspa]","^":"[Pexp]","+":"[Pplu]","-":"[Pmin]","(":"[Plsb]",")":"[Prsb]","/":"[Pdiv]","{":"[Plbb]","}":"[Prbb]","\\":"[Pbeg]","=":"[Peql]","<":"[Ples]",">":"[Pbgr]",":":"[Pcol]","!":"[Pexc]","_":"[Psub]"}
def ReplaceVariable(s):
    s = "]"+s+"["
    #print(s)
    cnt = 0;
    for g in variable_list:
        work = 0
        for i in range(len(s)-len(g)-1):
            if (((s[i]!=']') or (s[i+len(g)+1]!='['))):
                continue;

            if(s[i+1:i+len(g)+1]==g):
                if(work==0):
                    work=1
                    cnt+=1
                s =s[:i+1]+"%|||{}|||%".format(cnt)+s[i+len(g)+1:]
    s = s[1:-1]
    for i in range(1,cnt+1):
        s = s.replace("%|||{}|||%".format(i),"[var{}]".format(i))
    return s

def ReplacePunctuation(s):
    s = s.replace('[',"%temp%").replace("]","[Prmb]").replace("%temp%","[Plmb]")
    for i in punc_to_token:
        if(i!='[' and i !=']'):
            s = s.replace(i,punc_to_token[i])
    return s

def ReplaceVariableDes(s:str):
    cnt = 0;
    for u in variable_list:
        v = " "+u+" ";
        if(len(re.findall(r"(^{}[^a-zA-Z0-9])|([^a-zA-Z0-9]{}[^a-zA-Z0-9])|([^a-zA-Z0-9]{})$".format(u,u,u),s))>0):
            cnt+=1
            s = re.sub(r"(^)"+u+r"([^a-zA-Z0-9])",r"\1|||{}|||\2".format(cnt),s)
            s = re.sub(r"([^a-zA-Z0-9])"+u+r"([^a-zA-Z0-9])",r"\1|||{}|||\2".format(cnt),s)
            s = re.sub(r"([^a-zA-Z0-9])"+u+r"($)",r"\1|||{}|||\2".format(cnt),s)
    for i in range(1,cnt+1):
        s = s.replace("|||{}|||".format(i),"[var{}]".format(i))
    return s;
s = input()

print(ReplaceVariableDes(s))
print(ReplaceVariable(ReplacePunctuation(s)))
