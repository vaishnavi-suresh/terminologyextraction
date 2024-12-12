import re

def precision(guess, groundTruth):
    truePos = 0
    falsePos = 0
    for i in range(len(guess)):
        if guess[i] in groundTruth:
            truePos +=1
        else:
            falsePos+=1
    return truePos/(falsePos+truePos)

def recall(guess, groundTruth):
    truePos = 0
    falseNeg = 0
    for i in range(len(groundTruth)):
        if groundTruth[i] in guess:
            truePos +=1
        else:
            falseNeg +=1
    return truePos/(falseNeg+truePos)
def getKeywords(fp,numExtracted):
    groundTruths = []
    with open (fp,"r") as groundFile:
        allGroundText = groundFile.readlines()
        numArticles = 1
        for i in range(len(allGroundText)):
            allGroundText[i] = re.sub('\n','',allGroundText[i])
            allGroundText[i] = re.sub(f':\s[0-9](\.)*[0-9,\.]*','',allGroundText[i])
            allGroundText[i] = allGroundText[i].lower()
        for i in range(len(allGroundText)):
            if f'article' in allGroundText[i]:
                
                j = i+1
                article = []
                while j-i<numExtracted+1 and '' !=allGroundText[j]:
                    article.append(allGroundText[j])
                    j+=1

                groundTruths.append(article)
                numArticles  +=1
    return groundTruths
        


def f1(precision,recall):
    if precision!=0 and recall != 0:
        return 2/(1/recall+1/precision)
    return 0

def main():

    """
    with open ('../results/groundTruth.txt',"r") as groundFile:
        allGroundText = groundFile.readlines()
        numArticles = 1
        for i in range(len(allGroundText)):
            allGroundText[i] = re.sub('\n','',allGroundText[i])
        for i in range(len(allGroundText)):
            if f'article' in allGroundText[i]:
                print(True)
                
                j = i+1
                article = []
                while j<len(allGroundText ) and '' !=allGroundText[j]:
                    article.append(allGroundText[j])
                    j+=1

                groundTruths[f'article {numArticles}']=article
                numArticles  +=1
        

        print(groundTruths)
    """
    truthWords = getKeywords('../results/groundTruth.txt',15)
    modelWords = getKeywords('../results/results2.txt',15)

    allPrecision = 0
    allRecall = 0
    allFScore = 0
    with open('../results/metrics.txt','w', encoding='utf-8') as metrics:
        for i in range(len(truthWords)):
            
            truthArr = truthWords[i]
            modelArr = modelWords[i]
            print(truthWords)
            print(modelWords)
            pr = precision(modelArr,truthArr)
            rec = recall(modelArr,truthArr)
            fscore = f1(pr,rec)
            allPrecision += pr
            allRecall += rec
            allFScore += fscore
            metrics.write(f'ARTICLE {i+1}: precision: {pr} recall = {rec} f1 = {fscore}\n\n')
        metrics.write(f'TOTAL: precision: {allPrecision/10} recall: {allRecall/10} fscore: {allFScore/10}')
        

            


        

    #with open('../results/metrics2.txt',"w", encoding = 'utf-8') as outp:

if __name__ == "__main__":
    main()



