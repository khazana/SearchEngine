from snippetGenerationWithHL import extractSnippetFromFulltext
from stopwords import remStopWords

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
    
listOfFiles = ['CACM-2371.txt', 'CACM-1591.txt', 'CACM-1033.txt', 'CACM-1519.txt', 'CACM-1304.txt']

queryToSearch = "what articles exist which deal with tss time sharing system an operating system for ibm computers"

targetPath = "/home/itsmanasmohanty/IRProject/result.html"

generateHTMLFile(listOfFiles, queryToSearch, targetPath)
