import math
import os
import sys
import pickle
import nltk


#change index and corpus if stemming is required
indexer = pickle.load( open( "unigrams.pickle", "rb" ) )
#indexer = pickle.load( open( "stemmed_indexer.pickle", "rb" ) )

corpusdir = '/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/'
#corpusdir = '/Users/fathimakhazana/Documents/IRFinalProject/StemmedParsedFiles/'

#change in case expansion is required
query_file = "queries_expanded_pseudo.pickle"


N = 3204

def getStopWordslist():
    with open('/Users/fathimakhazana/Documents/IRFinalProject/common_words.txt', 'r') as f:
        stop_words = f.readlines()
    for i in range(0,len(stop_words)):
        stop_words[i] = stop_words[i].strip().lower()
    return stop_words

  
def remStopWords(text,stop_words):
    words = text.split()
    finaltext = ""
    for r in words: 
        if not r.lower() in stop_words: 
            finaltext  = finaltext + " " + r
    return finaltext

def get_queries_list(mode):
    if mode == 'stopped':
        stop_words = getStopWordslist()
        queries_dict = pickle.load( open( query_file, "rb" ) )
        queries = []
        for k,v in  sorted(queries_dict.items()):
            queries.append(v)
        queries = [remStopWords(q,stop_words) for q in queries]
        queries = [ " ".join(q.split()) for q in queries]
    elif mode =='stemmed':
        queries = []
        queries  = open('cacm_stem.query.txt', "r").readlines()
        queries = [q.strip() for q in queries]
    elif mode =='normal':
        queries_dict = pickle.load( open(query_file, "rb" ) )
        queries = []
        for k,v in  sorted(queries_dict.items()):
            queries.append(v)
    return queries

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
                file_content = open(corpusdir + file).read()
                tokens = nltk.word_tokenize(file_content)
                for term in query_terms:
                    tf = tokens.count(term)/len(tokens)
                    idf = math.log(N/len(indexer[term]))
                    s += tf*idf
                scores[file] = round(s, 4)
        return sorted(scores.items(), key=lambda kv: kv[1],reverse=True)
    else:
        return print("\nNo results found for",query, "!")
           
def main():
     #queries have three modes: stopped, stemmed and normal
    #for expanded queries, setting is normal with expandede query pickle file
    results = {}
    queries_list = get_queries_list('normal')
    sys.stdout = open("tf-idf.txt", "w")
    for index,query in enumerate(queries_list):
        results[query] = []
        s = score_documents(query)
        if s:
            print('\n')
            print("Query: ",query)
            for i,result in enumerate(s):
                results[query].append(result[0])
            for i,result in enumerate(s[:100]):
                rank = int(i) + 1
                print(index+1, " Q0 ",result[0]," ",rank," ",result[1]," tf-idf")
    with open('tfidf.pickle','wb') as f:
        pickle.dump(results,f)

if __name__ == "__main__":
    main()
