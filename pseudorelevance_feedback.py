import pickle
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import nltk
from collections import defaultdict, Counter
import csv


relevance = {}

corpusdir = '/home/dhaval/Acads/Spring19/Information Retrieval/Project/Parsed_Files/'

newcorpus = PlaintextCorpusReader(corpusdir, '.*')

with open('Pickles/unigrams.pickle','rb') as f:
    unigrams = pickle.load(f)

with open('Pickles/parsed_queries.pickle','rb') as f:
    queries = pickle.load(f)

with open('Pickles/relevance.pickle','rb') as f:
    rel = pickle.load(f)

with open('Pickles/tfidf.pickle','rb') as f:
    ranking = pickle.load(f)


def get_Tokens(filename):
    file_content = open(corpusdir + filename).read()
    tokens = nltk.word_tokenize(file_content)
    return tokens

def removeNumeric(l):
    k = []
    for word in l:
        if not(word.isnumeric()):
            k.append(word)
    return k


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

def expand_query():
    most_common = {}
    for key,value in ranking.items():
        index_key = list(ranking.keys()).index(key)+1
        top_doc_list =  []
        if index_key in relevance.keys():
             top_doc_list = relevance[index_key]
             if len(top_doc_list) > 10:
                 top_doc_list = top_doc_list[:10]
             elif len(top_doc_list) < 10:
                 for i in range(0,10):
                     if ranking[key][i] not in top_doc_list:
                         top_doc_list.append(ranking[key][i])
                     if len(top_doc_list) > 10:
                         top_doc_list=top_doc_list[:10]
        else:
            top_doc_list = value[:10]
        tokens = []
        for doc in top_doc_list:
            tokens = tokens + (get_Tokens(doc))
        tokens = removeNumeric(tokens)
        counter = Counter(tokens)
        most_occur = counter.most_common(50)
        words_in_query = queries[index_key]
        most_common[index_key] = top_words(most_occur,words_in_query,5)
    queries_expanded = {}
    for key, value in queries.items():
        l = value.split()
        l = l + most_common[key]
        queries_expanded[key] = ' '.join(l)

    with open('queries_expanded.csv', 'w') as csv_file:
       writer = csv.writer(csv_file)
       for key, value in queries_expanded.items():
           writer.writerow([key, value])
    with open('Pickles/expanded_queries_pseudo.pickle','wb') as f:
            pickle.dump(queries_expanded,f)


def main():

    for key,value in rel.items():
        val = []
        for v in value:
            val.append(v+".txt")
        relevance[int(key)] = val
    expand_query()


if __name__ == "__main__":
    main()
