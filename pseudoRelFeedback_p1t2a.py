#!/usr/bin/env python
# coding: utf-8

# In[84]:


import pickle
from collections import defaultdict
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import os
import numpy as np
import operator
import pandas as pd
from collections import defaultdict, Counter
from operator import itemgetter
import nltk
import json


# In[85]:


corpusdir = "/home/dhaval/Acads/Spring19/Information Retrieval/Project/Parsed_Files/"


# In[86]:


newcorpus = PlaintextCorpusReader(corpusdir, '.*')


# In[87]:


def get_Tokens(filename):
    file_content = open(corpusdir + filename).read()
    tokens = nltk.word_tokenize(file_content)
    return tokens


# In[88]:


with open('unigrams.pickle','rb') as f:
    unigrams = pickle.load(f)


# In[89]:


with open('parsed_queries.pickle','rb') as f:
    queries = pickle.load(f)


# In[90]:


with open('relevance.pickle','rb') as f:
    rel = pickle.load(f)


# In[91]:


with open('common_words') as f:
    content = f.read()
    stop_list = nltk.word_tokenize(content)


# In[92]:


stop_list.append('cacm')


# In[93]:


def removeStopWords(l):
    k = []
    for word in l:
        if word not in stop_list and not(word.isnumeric()):
            k.append(word)
    return k


# In[94]:


relevance = {}


# In[95]:


for key,value in rel.items():
    val = []
    for v in value:
        val.append(v+".txt")
    relevance[int(key)] = val


# In[96]:


tot_length = 0


# In[97]:


for filename in newcorpus.fileids():
    count = len(open(corpusdir+filename).readlines(  ))
    tot_length+=count


# In[98]:


avdl = tot_length/3204
k1=1.2
b=0.75
k2=100
N = 3204


# In[99]:


def getr(term,qid):
    list_of_docs = list(map(itemgetter(0), unigrams[term]))
    relevant_docs = relevance[qid]
    r = list(set(list_of_docs).intersection(set(relevant_docs)))
    return len(r)


# In[100]:


def getRanking(qid,query,t):
    try:
        R = len(relevance[qid])
    except:
        R = 0
    terms = query.split()
    query_id = qid
    frequency = defaultdict(int)
    for word in removeStopWords(terms):
        frequency[word]+=1
    Score = defaultdict(float)
    for term in frequency.keys():
        l = unigrams[term]
        qf = frequency[term]
        if(R!=0):
            r = getr(term,qid)
        else:
            r = 0
        n = len(l)
        for doc in l:
            dl = len(open(corpusdir+doc[0]).readlines())
            K = k1*((1-b)+b*dl/avdl)
            f = doc[1]
            d = (r+0.5)*(N-n-R+r+0.5)/((R-r+0.5)*(n-r+0.5))
            BM25 = np.log(d)*(k1+1)*f*(k2+1)*qf/((K+f)*(k2+qf))
            Score[doc[0]]+=BM25
    sorted_Score = sorted(Score.items(), key=operator.itemgetter(1), reverse = True)
    column_names = ['doc_id','BM25_score']
    df = pd.DataFrame(sorted_Score[0:t],columns = column_names)
    df.insert(1, "rank", np.arange(len(df))+1, True)
    df['system_name'] = "BM25"
    df.insert(0, "Q0", "Q0", True)
    df.insert(0, "query_id", query_id, True)
    return df
    #df.to_csv("query_"+str(query_id)+"_rankings_.csv",index=False)


# In[101]:


top_docs = {}
for key,value in queries.items():
    df = list(getRanking(key,value,10)['doc_id'])
    top_docs[key] = df


# In[102]:


def top_words(most_occur,words_in_query,k):
    i = 0
    l = []
    for word in most_occur:
        if(word[0] not in words_in_query.split()):
            i = i+1
            l.append(word[0])
        if i==k:
            break
    return l


# In[103]:


most_common = {}
for key,value in top_docs.items():
    tokens = []
    for doc in value:
        tokens = tokens + (get_Tokens(doc))
    tokens = removeStopWords(tokens)
    counter = Counter(tokens)
    most_occur = counter.most_common(50)
    words_in_query = queries[key]
    most_common[key] = top_words(most_occur,words_in_query,5)    


# In[104]:


queries_expanded = {}
for key, value in queries.items():
    l = value.split()
    l = l + most_common[key]
    queries_expanded[key] = ' '.join(l)


# In[105]:


with open('queries_expanded.json', 'w') as fp:
    json.dump(queries_expanded, fp)


# In[106]:


for key,value in queries_expanded.items():
    df = getRanking(key,value,50)
    df.to_csv("Query_expansion_results/query_"+str(key)+"_rankings_.csv",index=False)

