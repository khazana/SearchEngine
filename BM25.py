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

corpusdir = '/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/'

queries_list = ['recursive and programming','science', 'pizza']

#parameters for BM25
k1 =1.2
b =0.75
k2 = 100
R = 0.0
ri = 0.0
N = 3205

 
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
        
             
def score_documents(document_length_dict, avdl, query):
    files = [i for i in os.listdir(corpusdir) if i.endswith(".txt")]
    query_terms = query.split()
    query_terms = [q.lower() for q in query_terms]
    #check if atleast one term exists in the indexer
    query_terms = prune_keys(query_terms)
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
    document_length_dict = find_length_of_doc()
    avdl = round(mean(list(document_length_dict.values())))
    sys.stdout = open("BM25.txt", "w")
    for index,query in enumerate(queries_list):
        s = score_documents(document_length_dict, avdl, query)
        if s:
            print('\n')
            print("Query: ",query)
            for i,result in enumerate(s[:100]):
                rank = int(i) + 1
                print(index+1, " Q0 ",result[0]," ",rank," ",result[1]," BM25")

if __name__ == "__main__":
    main()