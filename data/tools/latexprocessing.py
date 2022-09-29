def stripback(rlatex,ch):
    while(rlatex[-1]==ch):
        rlatex = rlatex[0:-1]
    return rlatex


def norm(rlatex):
    if(len(rlatex)==0):
        return ""
    if("Wiki" in rlatex):
        return ""
    if(rlatex.startswith(r"{\displaystyle")):
        rlatex = rlatex[15:-1]
    if(rlatex.startswith(r"{\textstyle")):
        rlatex = rlatex[11:-1]
    if(rlatex.startswith(r"{\begin{aligned}")):
        rlatex = rlatex[16:-14]
    rlatex.replace(r"\left",'')
    rlatex.replace(r"\right",'')
    for i in range(5):
        rlatex = rlatex.strip(' ')
        rlatex = stripback(rlatex,'\\')
        rlatex = stripback(rlatex,'!')
        rlatex = rlatex.strip(',')
        rlatex = rlatex.strip('.')
    return rlatex;