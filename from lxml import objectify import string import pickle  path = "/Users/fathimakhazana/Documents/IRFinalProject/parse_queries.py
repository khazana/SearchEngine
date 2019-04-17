from lxml import objectify
import string
import pickle

path = "/Users/fathimakhazana/Documents/IRFinalProject/cacm.query.txt"

xml_string = open(path, "r").read()

root = objectify.fromstring(xml_string)
queries = {}

for i in range(0,64):
    s = root["DOC"][i]["DOCNO"][0].tail
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = s.strip().lower()
    s = s.replace('\n',' ')
    queries[i+1] = s

with open('parsed_queries.pickle','wb') as f:
    pickle.dump(queries,f)
