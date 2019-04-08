from bs4 import BeautifulSoup
import os
from collections import defaultdict
import json
import re

#global dictionaries which contains terms as the key and values 
#are in the form (docID1,term_count),(docID2,term_count)]
unigram_term = {}
bigram_term = {}
trigram_term = {}

path_to_corpus = '/Users/fathimakhazana/Documents/IRFinalProject/cacm/'


#dictionary which contains document ID as key and number of unigrams in it as value
term_count = {}
term_count= defaultdict(lambda: 0, term_count)
        

#returns list of ngrams which were saved to files in 'extract_terms.py'
def get_ngrams_list_from_file():
      f = open('unigrams.txt', 'r')
      unigrams_list = f.readlines()
      unigrams_list = [t.strip() for t in unigrams_list]
      f.close()
    
      f = open('bigrams.txt', 'r')
      bigrams_list = f.readlines()
      bigrams_list = [t.strip() for t in bigrams_list]
      f.close()
      
      f = open('trigrams.txt', 'r')
      trigrams_list = f.readlines()
      trigrams_list = [t.strip() for t in trigrams_list]
      f.close()
      
      return unigrams_list,bigrams_list,trigrams_list

def get_document_ID(file):
    docID = file.split('_raw.txt')
    docID = docID[0]
    return docID
 
#extract appropriate text from webpage from saved raw HTML files       
def extract_text_from_raw_HTML(rawfile):
    fh = open(rawfile,"rb")
    contents = fh.read().decode(errors='replace')
    soup = BeautifulSoup(contents,"html.parser")
    soup = soup.find("div", {"class":"mw-body"})
    if soup.find('div', id="toc"):
        soup.find('div', id="toc").decompose()
    if soup.find('div', {"class":"reflist"}):
        soup.find('div', {"class":"reflist"}).decompose()
    if soup.find_all("div", {'class':'navbox'}): 
        for div in soup.find_all("div", {'class':'navbox'}): 
            div.decompose()
    text = soup.text
    text = text.lower()
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    return text
    
#find unigrams which occur in a document    
#tern_count saves the number of unigrams in a document
def find_unigrams_in_document(text,unigrams_list,docID):
    for unigram in unigrams_list:
        unigram = " " + unigram + " "
        if unigram in text:
            unigram_term.setdefault(unigram,[]).append((docID, text.count(unigram)))
            count = term_count[docID]
            term_count[docID] = count + text.count(unigram)
            

          
            
#main function which creates the inverted index      
def inverted_indexer():
    files = [i for i in os.listdir(path_to_corpus) if i.endswith(".html")]
    unigrams_list =  get_ngrams_list_from_file()
    for file in files:
        docID = get_document_ID(file)
        text = extract_text_from_raw_HTML(path_to_raw_files + file)
        find_unigrams_in_document(text,unigrams_list,docID)
    
        
#save dictionaries to text file
def write_dict_to_file():
    f = open('InvertedLists/unigram_indexer.txt', 'w+')
    f.write(json.dumps(unigram_term))


inverted_indexer()
write_dict_to_file()

        
        