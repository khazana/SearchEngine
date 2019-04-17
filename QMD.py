import math
import os
import sys
import pickle
import nltk

indexer = pickle.load( open( "unigrams.pickle", "rb" ) )

corpusdir = '/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/'

N = 3205

def get_queries_list():
    queries_dict = pickle.load( open( "parsed_queries.pickle", "rb" ) )
    queries = []
    for k,v in queries_dict.items():
        queries.append(v)
    return queries

def get_collection_dict():
    collection = {}
    for key,values in indexer.items():
        s = 0
        for v in values:
            s+= v[1]
        collection[key] = s
    return collection


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
        
             
def score_documents(query):
    collection = get_collection_dict()
    document_length = find_length_of_doc()
    C = sum(collection.values())
    m = 2000
    files = [i for i in os.listdir(corpusdir) if i.endswith(".txt")]
    query_terms = query.split()
    query_terms = [q.lower() for q in query_terms]
    #check if atleast one term exists in the indexer
    query_terms = prune_keys(query_terms)
    if query_terms:
        scores = {}
        for file in files:
            if(check_if_doc_relevant(file,query_terms)):
                D = document_length[file]
                s = 0
                file_content = open(corpusdir + file).read()
                tokens = nltk.word_tokenize(file_content)
                for term in query_terms:
                    fqi = tokens.count(term)
                    cqi = collection[term]
                    s += math.log((fqi + m*(cqi/C))/(D + m))
                scores[file] = round(s, 4)
        return sorted(scores.items(), key=lambda kv: kv[1],reverse=True)
    else:
        return print("\nNo results found for",query, "!")
           
def main():
    queries_list = get_queries_list()
    sys.stdout = open("QLMD.txt", "w")
    for index,query in enumerate(queries_list):
        s = score_documents(query)
        if s:
            print('\n')
            print("Query: ",query)
            for i,result in enumerate(s[:100]):
                rank = int(i) + 1
                print(index+1, " Q0 ",result[0]," ",rank," ",result[1]," QLMD")

if __name__ == "__main__":
    main()
