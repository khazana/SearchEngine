import pickle

rel = {}
relevance = open('cacm.rel.txt', "r").readlines()
for item in relevance:
    query_no = item.split('Q0')[0].strip()
    document = item.split('Q0')[1].split(' 1')[0].strip()
    rel.setdefault(query_no,[]).append(document)
    
with open('relevance.pickle','wb') as f:
    pickle.dump(rel,f)
    
