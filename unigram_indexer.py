
import os
from collections import defaultdict
import pickle
import nltk

corpusdir = "/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/"

def get_Tokens(filename):
    file_content = open(corpusdir + filename).read()
    tokens = nltk.word_tokenize(file_content)
    return tokens

unigrams = defaultdict(list)

for filename in os.listdir(corpusdir):
    count = defaultdict(int)
    for word in get_Tokens(filename):
        count[word]+=1
    for word in count.keys():
        unigrams[word].append([filename,count[word]])
        
with open('unigrams.pickle','wb') as f:
    pickle.dump(unigrams,f)