import ast
import math
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
from statistics import mean 
import sys
import pickle
import nltk


indexer = pickle.load( open( "unigrams.pickle", "rb" ) )
relevance = pickle.load( open( "relevance.pickle", "rb" ) )


corpusdir = '/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/'

#parameters for BM25
k1 =1.2
b =0.75
k2 = 100
N = 3204

def get_queries_list():
    queries_dict = pickle.load( open( "parsed_queries.pickle", "rb" ) )
    queries = []
    for k,v in sorted(queries_dict.items()):
        queries.append(v)
    return queries

 
def find_length_of_doc():
    document_length = {}
    files = [i for i in os.listdir(corpusdir) if i.endswith(".txt")]
    for file in files: 
            file_content = open(corpusdir + file).read()
            tokens = nltk.word_tokenize(file_content)
            document_length[file] = len(tokens)
    return document_length



def check_if_doc_relevant(docID,query_terms):
    flag = 0
    for term in query_terms:
        documents = indexer[term]
        documents = [d[0] for d in documents]
        if docID in documents:
            flag += 1
    if flag > 0:
        return True
    else:
        return False

def prune_keys(query_terms):
    keys = list(indexer.keys())
    filtered_query_terms = []
    for term in query_terms:
        if term in keys:
            filtered_query_terms.append(term)
    return filtered_query_terms
        
 
def find_relevant_docs(query_index):
    rel_list = list(relevance.keys())
    if str(query_index + 1) in rel_list:
        return relevance[str(query_index + 1)]
    else:
        return []
    
def find_ri(relevant_docs,term):
    if relevant_docs:
        r = []
        term_docs = indexer[term]
        for doc in relevant_docs:
            for t in term_docs:
                if doc +'.txt' == t[0]:
                    r.append(doc)
        return len(r)
    else:
        return 0.0
            
            
def score_documents(query_index,document_length_dict, avdl, query):
    files = [i for i in os.listdir(corpusdir) if i.endswith(".txt")]
    query_terms = query.split()
    query_terms = [q.lower() for q in query_terms]
    #check if atleast one term exists in the indexer
    query_terms = prune_keys(query_terms)
    relevant_docs = find_relevant_docs(query_index)
    if relevant_docs:
        R = len(relevant_docs)
    else:
        R = 0.0
    if query_terms:
        scores = {}
        for file in files:
            if(check_if_doc_relevant(file,query_terms)):
                s = 0
                dl = document_length_dict[file]
                K = k1 * ((1-b) + b * (dl/avdl))
                file_content = open(corpusdir + file).read()
                tokens = nltk.word_tokenize(file_content)
                for term in query_terms:
                    ri = find_ri(relevant_docs,term)
                    ni = len(indexer[term])
                    qfi = query_terms.count(term)
                    fi = tokens.count(term)
                    first_term = math.log( ( (ri + 0.5) / (R - ri + 0.5) ) / ( (ni - ri + 0.5) / (N - ni - R + ri- + 0.5)) )
                    second_term = ((k1 + 1) * fi) / (K + fi)
                    third_term = ((k2+1) * qfi) / (k2 + qfi)
                    s += first_term  * second_term  * third_term 
                scores[file] = round(s, 4)
        return sorted(scores.items(), key=lambda kv: kv[1],reverse=True)
    else:
        return print("\nNo results found for",query, "!")
           
def main():
    results = {}
    queries_list = get_queries_list()
    document_length_dict = find_length_of_doc()
    avdl = round(mean(list(document_length_dict.values())))
    sys.stdout = open("BM25.txt", "w")
    for index,query in enumerate(queries_list):
        results[query] = []
        s = score_documents(index,document_length_dict, avdl, query)
        if s:
            print('\n')
            print("Query: ",query)
            for i,result in enumerate(s):
                results[query].append(result[0])
            for i,result in enumerate(s[:100]):
                rank = int(i) + 1
                print(index+1, " Q0 ",result[0]," ",rank," ",result[1]," BM25")
    with open('BM25.pickle','wb') as f:
        pickle.dump(results,f)

if __name__ == "__main__":
    main()
