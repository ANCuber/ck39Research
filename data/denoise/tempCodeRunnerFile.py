
            postext = postext.replace("\\text","")
            postext = postext.replace("\\tfrac","\\frac")
            if(postext[-1]=='\\'):
                postext = postext[0:-2]
            if(postext[-1]==','):
                postext = postext[0:-2]
            postext= postext+'\n'
            with open(writefiledir, "a",encoding='utf-8') as file_object:
                file_object.write(postext)


