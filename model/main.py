"""
1. Create a function that tags the words in the cleaned data. 
2. Use CBOW from word2vec library to compute word embeddings - pip
3. use YAKE to extract yake keywords 
4. for each YAKE keyword, split each of the top 1000 keywords into adjectives and nouns. Place them into a list
5. TBD on implementation, use the word2vec graph to get the words closest in distance. Return top 20
TO DO: remove stopwords
"""

from gensim.models import Word2Vec
from gensim.parsing.preprocessing import remove_stopwords
import pke 
import re

import pke.unsupervised
import dataCleaner as dc
import string
import nltk
from nltk.corpus import stopwords
from yake import KeywordExtractor
import numpy as np
import electionTerms


class key:
    def __init__ (self):
        self.np = r'(NN|NNS)+'
        self.pn = r'(NNP|NNPS)+'
        #self.vb = r'(VB|VBD|VBG|VBN|VBP|VBZ)'
        #self.jj = r'JJR?S?'
        #self.vp = r'(IN)?(RBS?)*(VBD?G?N?P?Z?)(RBD?)'
        self.patterns = [self.np,self.pn]
        self.unacceptable =  ["CC", "RB", "RBR", "RBS", "DT", "PDT", "PRP", "PRP$", "WP", "WP$", "IN"]
        

    def allPOS(self):
        return self.patterns


def yakeKeywords(str,sl):
    
    strArr = str.split("\n")
    allKeywords = []
    for entry in strArr:
        KE = pke.unsupervised.YAKE()
        KE.load_document(str, language = 'en', normalization=None,stoplist=sl)
        KE.candidate_selection(n=8)
        KE.candidate_weighting(window=4,use_stems=False)
        toAppend = KE.get_n_best(n=50, threshold=0.45)
        
        allKeywords.append(toAppend)


    return allKeywords

def isValid (wp):
    """
    Get 5 -15 keywords from the test, based on the following requirements
Up to  consecutive words unless long proper noun
No more than one entity
Noun phrase, proper name, verb, adj, phrasal verb, or part of clause
No full sentences, conjunctions, adverbs, determiner, number, preposition, or pronoun
No base form
Only one word for each concept

    """
    tokens = nltk.word_tokenize(wp)
    tagged_tokens = nltk.pos_tag(tokens)
    tags = []
    keys = key()
    all = keys.allPOS()
    for item in tagged_tokens:
        tags.append(item[1])
    for i in range(len(tags)):
        if tagged_tokens[i][1] in keys.unacceptable:
            return None
  
        
    
    tagString = "".join([tag for tag in tags])
    for k in all:
        pattern = re.compile(k)
        if pattern.match(tagString):
            return item
    return None


def yakeRanking (w2v, allText,sl):
    
    yakekeys = np.array(yakeKeywords(allText,sl),dtype = object)
    flat = [item for sublist in yakekeys for item in sublist]
    rank = sorted(flat,key = lambda x:x[1])
    kw = {}
    w2vSims = {}
    indexArr = []
    
   # print(rank[:500])
    i=0
    rankNum =0
    min = float(rank[0][1]) if rank else 1.0
    while rankNum<len(rank):
        p=rank[rankNum]
        if isValid(p[0]):
            kw[p[0]]=p[1]
            indexArr.append(p[0])
            if float(p[1])<min:
                min = p[1]
            i+=1
        rankNum+=1

    et = electionTerms.electionTerms


    for key in indexArr:
        indivwords = key.split()


        similarity = 0.001
        for word in indivwords:
            for term in et:
                if term in w2v.wv.key_to_index and word in w2v.wv.key_to_index:
                    similarity *= (w2v.wv.similarity(word,term)+0.001)
        print(similarity)
        print(min)
        w2vSims[key]=1/(kw[key]+0.001)+20*similarity/(min+0.001)
    print(w2vSims)
    rankwtv = sorted(w2vSims.items(), key=lambda x: x[1],reverse=True)
    return rankwtv
        



def main():
    #extractor = pke.unsupervised.YAKE()
    allText = dc.cleantext('../corpuses/training.txt')
    allText = allText.lower()
    sentences = dc.splitLines(allText)
    sw = set(stopwords.words('english'))
    news_stopwords = set([
    "breaking", "news", "journal", "times", "post", "herald", "gazette", 
    "daily", "weekly", "monthly", "article", "editorial", "press", "media", 
    "report", "reporting", "publication", "columnist", "coverage", "network", 
    "wire", "agency", "source", "sources", "headline", "reuters","nbc", "associated", "follow", "nbcfollow","subscribe","like","comment",
    "ap", "nytimes", "cnn", "bbc", "fox", "npr", "bloomberg", "politico", "marie claire"
    "wsj", "guardian", "telegraph", "tribune","magazine","'re"])
    custom_stopwords = set([
    "'re", "'ve", "'ll", "'d", "'m", "'s", "n't", 
    'a', 'an', 'the',            
    'and', 'or', 'but', 'if', 'while', 'because',
    'to', 'of', 'in', 'on', 'at', 'with', 'by', 
    'he', 'she', 'it', 'they', 'we', 'you', 'i',
    'is', 'was', 'were', 'be', 'been', 'are', 
    'that', 'this', 'there', 'here'
    "is", "was", "are", "were", "am", "be", "been", "being",
    "can", "could", "shall", "should", "will", "would", "may", "might", "must",
    "do", "does", "did", "have", "has", "had", "get", "got", "make", "made",
    "take", "took", "go", "went", "come", "came", "say", "said", "see", "saw",
    "seen", "know", "knew", "known", "think", "thought", "tell", "told", "find",
    "found", "give", "given", "work", "worked", "use", "used", "try", "trying",
    "start", "starting", "begin", "beginning", "end", "ending", "ask", "asking",
    "keep", "keeping", "let", "letting", "help", "helping", "need", "needing",
    "want", "wanting", "like", "liking", "love", "loving", "hate", "hating",
    "seem", "seems", "seemed", "appear", "appears", "appeared", "become",
    "became", "look", "looks", "looked", "feel", "feels", "felt", "sound",
    "sounds", "sounded"])

    combinedStopwords = sw.union(news_stopwords).union(custom_stopwords)
    for i in range(len(sentences)):
        sentences[i] = remove_stopwords(s=sentences[i], stopwords=combinedStopwords)
        
    sentences = [line.translate(str.maketrans('', '', string.punctuation)).split() for line in sentences]

    w2v = Word2Vec(sentences = sentences, vector_size=100,window=5,min_count=5,sg=0)






    #KE = KeywordExtractor(stopwords=combinedStopwords,windowsSize=2, dedupLim=  0.5, top = 25,n=3)
    

    allIndivArticles = dc.cleanIndivArticle('../corpuses/test.txt')
    with open('../results/results.txt',"w",encoding = 'utf-8') as outp:
        for i in range(len(allIndivArticles)):
            outp.write(f'\n article {i+1}:\n')
            rankwtv = yakeRanking(w2v, allIndivArticles[i],combinedStopwords)
            for i in range(15):
                if i<len(rankwtv):
                    elem = rankwtv[i]
                    outp.write(f'{elem[0]}: {elem[1]}\n')
        

    
    
    
    






if __name__ == "__main__":
    main()