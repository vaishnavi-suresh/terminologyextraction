"""
The goal of this program is to use regex to clean the data
"""
import re
def cleantext(filepath):
    with open(filepath,"r", encoding = "utf8") as corpus:
        allLines = corpus.read()
        
        allLines= re.sub(r"(\bHEADER: \b)[A-Z, a-z,0-9,\/,\.,\-,\:]*\n\n(\bCONTENT: \b)","",allLines)
        
        allLines=re.sub(r'\b([A-Z](?:\.[A-Z]?:)*)\.?', lambda m: ''.join(m.group(0).split('.')), allLines)
        allLines=re.sub(':', ' ', allLines)
        allLines=re.sub("’", "'", allLines)
        allLines = re.sub(r'\b(\w+)\.(\w+)\b', r'\1. \2', allLines)
        return allLines
        
def splitLines(str):
    allLinesArray = re.split(r"\.|\n",str)
    return allLinesArray

def cleanLine(line):
    line= re.sub(r"(\bHEADER: \b)[A-Z, a-z,0-9,\/,\.,\-,\:]*\n\n","",line)
    line= re.sub(r"(\bCONTENT: \b)","",line)
    line=re.sub(r'\b([A-Z](?:\.[A-Z]?:)*)\.?', lambda m: ''.join(m.group(0).split('.')), line)
    line=re.sub(':', ' ', line)
    line=re.sub(" '", "'", line)
    line = re.sub(r'\b(\w+)\.(\w+)\b', r'\1. \2', line)
    return line

def cleanIndivArticle(filepath):
    allCleanedArticles = []
    with open(filepath,"r", encoding = "utf8") as corpus:
        allLines = corpus.read()
        allLines = allLines.split(f'\n')
        for i in range(len(allLines)):
            tojoin = ""
            j = i+2
            if "HEADER" in allLines[i]:
                while allLines[j]!='':
                    tojoin+=allLines[j]
                    j+=1
                tojoin = cleanLine(tojoin)
                allCleanedArticles.append(tojoin)
    return allCleanedArticles


