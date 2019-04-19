from pandas import DataFrame
import pandas as pd
import pickle

tables = []
pk_list = []
MAP_list  = []
MRR_list = []


run1 = pickle.load( open( "tfidf.pickle", "rb" ) )
run2 = pickle.load( open( "QMD.pickle", "rb" ) )
run3 = pickle.load( open( "BM25.pickle", "rb" ) )
run4 = pickle.load( open( "lucene.pickle", "rb" ) )
run5 = pickle.load( open( "tfidf_stopped.pickle", "rb" ) )
run6 = pickle.load( open( "QMD_stopped.pickle", "rb" ) )
run7 = pickle.load( open( "QMD_qe_pseudo.pickle", "rb" ) )
run8 = pickle.load( open( "QMD_qe_embedding.pickle", "rb" ) )
run9 = pickle.load( open( "BM25_stopped.pickle", "rb" ) )


runs = [(run1,'tfidf'),(run2,'qmd'),(run3,'bm25'),(run4,'lucene'),
        (run5,'tfidf_stopped'),(run6,'QMD_stopped'),(run7,'QLMD_qe_pseudo'),(run8,'QLMD_qe_embedding'),(run9,'BM25_stopped')]

relevance = pickle.load( open( "relevance.pickle", "rb" ))


def check_if_doc_relevant(doc,query_index):
    rel_docs = relevance[query_index+1]
    if doc in rel_docs:
        return True
    else:
        return False
   
    
def MRR(ranking_dict):
    rel_list = list(relevance.keys())
    rr=[]
    for k,v in ranking_dict.items():
        #list(ranking_dict.keys()).index(k)+1 gives query index
        if list(ranking_dict.keys()).index(k)+1 in rel_list:
            rel_docs = relevance[list(ranking_dict.keys()).index(k)+1]
            docs = ranking_dict[k]
            docs = docs[:100]
            flag = 1
            for index,d in enumerate(docs):
                if(flag):
                    if d.split('.txt')[0] in rel_docs:
                        rr.append(1/(index+1))
                        flag = 0
    MRR_list.append(round(sum(rr) /len(rr),4))


def MAP(ranking_dict):
    rel_list = list(relevance.keys())
    MAP= []
    for k,v in ranking_dict.items():
        #list(ranking_dict.keys()).index(k)+1 gives query index
        if list(ranking_dict.keys()).index(k)+1 in rel_list:
            precision = []
            result_docs = ranking_dict[k]
            result_docs = result_docs[:100]
            result_docs = [r.split('.txt')[0] for r in result_docs]
            b = []
            a = []
            p= 0
            for index,doc in enumerate(result_docs):
                b.append(doc)
                if( check_if_doc_relevant(doc,list(ranking_dict.keys()).index(k))):
                    a.append(doc)
                    p= len(list(set(a) & set(b)))/len(b)
                    precision.append(p) 
            avg_precision_per_query = round(sum(precision) / len(precision),4 )
            MAP.append(avg_precision_per_query)
    MAP_list.append(round(sum(MAP) / len(MAP),4))

                                
def precision_recall(ranking_dict):
    rel_list = list(relevance.keys())
    prec= []
    rec = []
    for k,v in ranking_dict.items():
        #list(ranking_dict.keys()).index(k)+1 gives query index
        if list(ranking_dict.keys()).index(k)+1 in rel_list:
            precision = []
            recall = []
            result_docs = ranking_dict[k]
            result_docs = result_docs[:100]
            result_docs = [r.split('.txt')[0] for r in result_docs]
            b = []
            a = []
            p= 0
            r = 0
            for index,doc in enumerate(result_docs):
                b.append(doc)
                if( check_if_doc_relevant(doc,list(ranking_dict.keys()).index(k))):
                    a.append(doc)
                if(a):
                    p= round(len(list(set(a) & set(b)))/len(b),4)
                    r = round((len(list(set(a) & set(b)))/len(relevance[list(ranking_dict.keys()).index(k)+1])),4)
                precision.append(p)
                recall.append(r)        
            prec.append(precision)
            rec.append(recall)
    return prec,rec
            
def create_spreadsheet_pr(precision,recall,file_name):
    import pandas as pd
    dataframes=[]
    rel_list = list(relevance.keys())
    for i in range(len(rel_list)):
        result = {}
        title = 'Query ' + str(i+1)
        result = {title: list(range(1, 101)),
                  'Precision':precision[i],
                  'Recall':recall[i]}
        df = DataFrame(result, columns= [title,'Recall', 'Precision'])
        dataframes.append(df)
    pd = pd.concat(dataframes, axis = 1)
    pd.to_excel('/Users/fathimakhazana/Documents/IRFinalProject/'+ file_name+ '.xlsx', index = None, header=True) #Don't forget to add '.xlsx' at the end of the path

def pk(precision,name):
    pk5 = []
    pk20 = []
    for i in range(0,52):
        pk5.append(precision[i][4]) 
        pk20.append(precision[i][19]) 
    p_k = [('Query', list(range(1,53))),
                 ('PK5', pk5),
                 ('PK20', pk20),]
    res = pd.DataFrame.from_items(p_k)
    pk_list.append(res)

  
def get_tables(run,name):
    p,r = precision_recall(run)
    create_spreadsheet_pr(p,r,name + '_precision_recall')
    MAP(run)
    MRR(run)
    pk(p,name+'_PK')

for i in runs:
    get_tables(i[0],i[1])
    

results = [('Retrivel Model', ['TF-IDF', 'QLM-Dirichlet', 'BM25','Lucene']),
         ('MAP', MAP_list),
         ('MRR', MRR_list),]

pd1 = pd.DataFrame.from_items(results)
pd1.to_excel('/Users/fathimakhazana/Documents/IRFinalProject/MAP-MRR' + '.xlsx', index = None, header=True) #Don't forget to add '.xlsx' at the end of the path

pd2 = pd.concat(pk_list, axis = 1)
pd2.to_excel('/Users/fathimakhazana/Documents/IRFinalProject/PK' + '.xlsx', index = None, header=True) #Don't forget to add '.xlsx' at the end of the path

