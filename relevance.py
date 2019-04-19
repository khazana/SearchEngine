import pickle

rel = {}
relevance = open('cacm.rel.txt', "r").readlines()
for item in relevance:
    query_no = int(item.split('Q0')[0].strip())
    document = item.split('Q0')[1].split(' 1')[0].strip()
    number = document.split('-')[1]
    number = "{0:04}".format(int(number))
    document = 'CACM-' + number
    rel.setdefault(query_no,[]).append(document)
    
with open('relevance.pickle','wb') as f:
    pickle.dump(rel,f)
    
