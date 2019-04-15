
import os
from collections import defaultdict
import pickle
import nltk

corpusdir = "/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/"
count = defaultdict(int)

def get_Tokens(filename):
    file_content = open(corpusdir + filename).read()
    tokens = nltk.word_tokenize(file_content)
    return tokens

for filename in os.listdir(corpusdir):
    for word in get_Tokens(filename):
        count[word]+=1
        
with open('tokens_frequency.pickle','wb') as f:
    pickle.dump(count,f)