from gensim.models import Word2Vec
import os
import nltk
import pickle
import operator
from collections import OrderedDict
import json


path ='/home/dhaval/Acads/Spring19/Information Retrieval/Project/Parsed_Files/'

def top_embeddings(most_occur,words_in_query,k):
    i = 0
    l = []
    for word in most_occur:
        if(word[0] not in words_in_query):
            i = i+1
            l.append(word)
        if i==k:
            break
    return l

def removeNumeric(l):
    k = []
    for word in l:
        if not(word.isnumeric()):
            k.append(word)
    return k

def get_Tokens(filename):
    file_content = open(path + filename).read()
    tokens = nltk.word_tokenize(file_content)
    return (tokens)

tokens = []
for file in os.listdir(path):
    tokens.append(get_Tokens(file))


model = Word2Vec(tokens, min_count=1)


with open('parsed_queries.pickle','rb') as f:
    queries = pickle.load(f)


queries_expanded = {}


for key,value in queries.items():
    query_terms = value.split()
    top_words = []
    expand = []
    for word in removeNumeric(query_terms):
        try:
            sim = model.wv.most_similar(word,topn=10)
        except:
            continue
        top_words+=top_embeddings(sim,query_terms,3)
        top_words = sorted(top_words, key = operator.itemgetter(1), reverse = True)
    t = [x[0] for x in top_words]
    expansion_terms = list(OrderedDict.fromkeys(t))[0:5]
    l = query_terms + expansion_terms
    queries_expanded[key] = ' '.join(l)

with open('expanded_queries_embedding.pickle','wb') as f:
        pickle.dump(queries_expanded,f)

with open('queries_expanded_embeddings.json', 'w') as fp:
    json.dump(queries_expanded, fp)
