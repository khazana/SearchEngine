#!/usr/bin/env python
# coding: utf-8

# In[140]:


from gensim.models import Word2Vec
import os
import nltk
import pickle
import operator
from collections import OrderedDict
import json


# In[141]:


path = "/home/dhaval/Acads/Spring19/Information Retrieval/Project/Parsed_Files/"


# In[142]:


with open('common_words') as f:
    content = f.read()
    stop_list = nltk.word_tokenize(content)
stop_list.append('cacm')


# In[143]:


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


# In[144]:


def removeStopWords(l):
    k = []
    for word in l:
        if word not in stop_list and not(word.isnumeric()):
            k.append(word)
    return k


# In[145]:


def get_Tokens(filename):
    file_content = open(path + filename).read()
    tokens = nltk.word_tokenize(file_content)
    return removeStopWords(tokens)


# In[146]:


tokens = []
for file in os.listdir(path):
    tokens.append(get_Tokens(file))


# In[147]:


model = Word2Vec(tokens, min_count=1)


# In[148]:


with open('parsed_queries.pickle','rb') as f:
    queries = pickle.load(f)


# In[152]:


queries_expanded = {}


# In[153]:


for key,value in queries.items():
    query_terms = value.split()
    top_words = []
    expand = []
    for word in removeStopWords(query_terms):
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


# In[154]:


with open('queries_expanded_embeddings.json', 'w') as fp:
    json.dump(queries_expanded, fp)

