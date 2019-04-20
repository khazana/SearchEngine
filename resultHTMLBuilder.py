from snippetGenerationWithHL import extractSnippetFromFulltext
from stopwords import remStopWords
import pickle

def generateHTMLFile(filelist,query,targetPath):
    f = open(targetPath,'w')
    qterms = list(set(remStopWords(query).split()))
    messageHeader = """<html>
    <head>Results</head>
    <body>"""
    messageFooter = """</body></html>"""
    
    messagebody = ""

    for entry in filelist:
        messagebody = messagebody + "<h3>" +entry +"</h3>"
        filepath = "/home/itsmanasmohanty/IRProject/CACM/test-collection/CACMTXT/" + entry
        fileToGet = open(filepath, 'r')
        fulltext = fileToGet.read()
        messagebody = messagebody + "<p>" + extractSnippetFromFulltext(fulltext,qterms,500) + "</p>"
    
    message = messageHeader + messagebody + messageFooter
    f.write(message)
    f.close()

docs   = pickle.load( open( "tfidf.pickle", "rb" ) )
queries = pickle.load( open( "parsed_queries.pickle", "rb" ) )

doclist = []
querylist = []

for key,val in docs.items():
    doclist.append(val[0:99])

for key,val in queries.items():
    querylist.append(val)

for i in range(0, len(querylist)):
    targetPath = "/home/itsmanasmohanty/IRProject/result"+"_"+str(i)+".html"
    generateHTMLFile(doclist[i],querylist[i] , targetPath)
