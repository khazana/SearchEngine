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
#2. Edit distance
#3.For words with same number of maximum letters in common and same minimum edit distance, sort according to frequency in collection
def spell_correct(query):
    first_letter = query[0]
    edit1 = []
    for term in index_words:
        if term[0] == first_letter and len(term) < len(query) + 2:
            common_elements = find_common_elements(term, query)
            edit1.append([term,common_elements,nltk.edit_distance(term, query),tokens_frequency[term]])
    candidates_list_1  = sorted(edit1, key = lambda x: int(x[1]), reverse =True)
    frequency = []
    for index,item in enumerate(candidates_list_1):
       frequency.append(item[3])
    for index,item in enumerate(candidates_list_1):
        candidates_list_1[index].append(round(max(frequency)*item[1] + (max(frequency)*(1/item[2])) + item[3]/max(frequency) ,4))
    candidates_list_2 = sorted(candidates_list_1, key = lambda x: int(x[4]), reverse =True)
    results = []
    candidates_list_2 = candidates_list_2[:6]
    for item in candidates_list_2:
        results.append(item[0])
    return results


query = 'scicne and math'
query_terms = query.split(' ')
for term in query_terms:
    if term not in index_words:
        correct_words = spell_correct(term)
        print("Did you mean")
        for word in correct_words:
            print(word)
