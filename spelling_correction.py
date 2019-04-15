import re
from collections import Counter
from nltk.corpus import words
import enchant
import pickle
import nltk


indexer = pickle.load(open("unigrams.pickle", "rb" ))

tokens_frequency = pickle.load(open( "tokens_frequency.pickle", "rb" ))

index_words =  list(indexer.keys())

def find_common_elements(str1, str2):
    str1_list = list(str1)
    str1_list.sort()
    str2_list = list(str2)
    str2_list.sort()
    return len(list(set(str1_list) & set(str2_list)))

#spell correction has criteria below in the following order of priority:
#1.find words with maximum letters in common
#2.For words, with same number of maximum letters in common, order them according to the edit distance
#3.For words with same number of maximum letters in common and same minimum edit distance, pick the word with maximum frequency
def spell_correct(query):
    first_letter = query[0]
    edit1 = []
    for term in index_words:
        if term[0] == first_letter and len(term) < len(query) + 2:
            common_elements = find_common_elements(term, query)
            edit1.append([term,common_elements,nltk.edit_distance(term, query),tokens_frequency[term]])
    candidates_list_1  = sorted(edit1, key = lambda x: int(x[1]), reverse =True)
    max_common = candidates_list_1 [0][1]
    candidates_list_2 = []
    for c in candidates_list_1 :
        if c[1] == max_common:
            candidates_list_2.append(c)
    candidates_list_2 =  sorted(candidates_list_2, key = lambda x: int(x[2]))
    min_edit= candidates_list_2 [0][2]
    candidates_list_3 = []
    for c in candidates_list_2:
        if c[2] == min_edit:
            candidates_list_3.append(c)
    candidates_list  = sorted(candidates_list_3, key = lambda x: int(x[3]), reverse =True)
    return candidates_list[0][0]

query = 'scne'
if query not in index_words :
    correct_word = spell_correct(query)
    print("Did you mean",correct_word, "?")


