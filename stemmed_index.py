import pickle
from string import punctuation
import os
from collections import defaultdict
import nltk

path = "/Users/fathimakhazana/Documents/IRFinalProject/cacm_stem.txt"
corpusdir = "/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/"               

                 
def remove_punctuations(content):
    content = ''.join(characters for characters in content if characters not in '!}{][)(\><=#"$%&,/*`\'')
    punc = punctuation.replace('-',"")
    content = ' '.join(token.strip(punc) for token in content.split() if token.strip(punc))
    content = ' '.join(token.replace("'", "") for token in content.split() if token.replace("'", ""))
    content = ' '.join(content.split())
    return content

def get_Tokens(index,stemmed_dict):
    tokens = nltk.word_tokenize(stemmed_dict[index + 1])
    return tokens

def create_corpus_dict(stem):
    stemmed_text = {} 
    for i in range(1,3205):
        stemmed_text[i] = remove_punctuations(stem[i])
    return stemmed_text

def create_index(stemmed_dict):
    files = os.listdir(corpusdir)
    files = [f for f in files if f.endswith('.txt')]
    stemmed_unigrams = defaultdict(list)
    for index,filename in enumerate(sorted(files)):
        count = defaultdict(int)
        for word in get_Tokens(index,stemmed_dict):
            count[word]+=1
        for word in count.keys():
            stemmed_unigrams[word].append([filename,count[word]])
    return stemmed_unigrams

    
def main():
    stemmed_corpus = open(path, "r").read()
    stemmed_corpus = stemmed_corpus.split('#')
    stemmed_dict = create_corpus_dict(stemmed_corpus)
    stemmed_index = create_index(stemmed_dict)       
    with open('stemmed_indexer.pickle','wb') as f:
        pickle.dump(stemmed_index,f)
    

if __name__ == "__main__":
    main()
