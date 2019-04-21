import os
import nltk
import pickle
import operator
from collections import OrderedDict
import json
from stemming.porter2 import stem
from nltk.corpus import wordnet
from collections import defaultdict, Counter


path ='/home/dhaval/Acads/Spring19/Information Retrieval/Project/Parsed_Files/'

with open('Pickles/parsed_queries.pickle','rb') as f:
    queries = pickle.load(f)
with open('Pickles/stemmed_indexer.pickle','rb') as f:
    stemmed = pickle.load(f)
with open('Pickles/unigrams.pickle','rb') as f:
    unigrams = pickle.load(f)

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

def removeWordsinQuery(expand,query_terms):
    l = []
    for word in expand:
        if word not in query_terms:
            l.append(word)
    return l

queries_expanded = {}
b = set(unigrams.keys())

for key,value in queries.items():
    query_terms = value.split()
    top_words = []
    expand = []
    for word in removeNumeric(query_terms):
        syns = wordnet.synsets(word)
        a = set([x.lemmas()[0].name() for x in syns])
        expand = expand + list(a.intersection(b))
    expand = removeWordsinQuery(expand,query_terms)
    counter = Counter(expand)
    most_occur = counter.most_common(10)
    l = query_terms + [x[0] for x in most_occur]
    queries_expanded[key] = ' '.join(l)

with open('Pickles/expanded_queries_thesaurus.pickle','wb') as f:
        pickle.dump(queries_expanded,f)

with open('expanded_queries_thesaurus.json', 'w') as fp:
    json.dump(queries_expanded, fp)
