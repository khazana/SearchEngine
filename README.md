# SearchEngine
This project consists of the following subtasks:

   1.Indexing and retrieval using different kinds of retrieval models and query enhancement techniques<br />
   2.Displaying the results<br />
   3.Evaluation with various measures<br />
   4.Extra credit<br />

1.Indexing and retrieval using different kinds of retrieval models and enhancement techniques:<br />
   a) To create the index, the following files are used:<br />
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) corpus_generator.py - This code will take the given collection of raw HTML files and create a set of clean and processed text files.<br />
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii) unigram_indexer.py - This code will use the set of generated corpora from corpus_generator.py to create an index stored as a dictionary. Keys are words and values are the array of tuples in the form (documentID, word_frequency).<br />
        
   b) Retrievel Models:<br />
    Queries:<br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;First, the given queries file has to be converted to a dictionary so that it can be used easily whenever required. This was done with the code in 'parse_queries.py'. This will save a dictionary as pickle file where keys are query ids and the value is the query.

   Relevance:<br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Next, the given relevance information also had to be stored for easy use. This was done with the code relevance.py. It will store the information in a pickle file as a dictionary where key is the query number and value is the list of relevant documents.
    
   Stopping:<br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;stopwords.py contains two functions which will take a string as input and return the string without stopwords. The stopwords list was built from the given list of common words. These two functions are included in the retrievel models whose runs are to be tested with stopping (tfidf and QLMD in our case).
        
   Stemming:<br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For stemming, there are two steps: <br />
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i)Creation of stemmed index - This is done with the code stemmed_index.py. This code will take the provided single stemmed corpus and create 3204 seperate files just like the non stemmed corpus set.<br /> 
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii)There are two lines of code which will read the queries from the stemmed query text file. This will be included whenever stemming is required.<br /> 

 Once the above steps are completed, the retrivel models are ready to be tested in all modes.<br />

 Three retrieval models have been implemented from scratch using the following files:<br />

i) tf-idf.py - This file has three modes: 'normal','stemmed' and 'stopped' for the get_queries_list(mode) function. If 'normal' is selected, the default queries are chosen for the run. If 'stopped' is chosen, queries go through stopping. If 'stemmed' is chosen, the stemmed queries are used. When mode 'stemmed' is chosen, mode must be 'stemmed' for the function set_index_corpus_path(mode), otherwise it should be set to 'normal'. This function will set the index and corpus path accordingly. The output of this file will be the following two:<br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; a) A text file under the same name containing the top 100 results for each of the 64 queries along with the score.<br />
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; b) A pickle file of a dictionary where key is a query and value is the list of all ranked documents.<br /><br />
        
ii) qmd.py - This file will have three modes: 'normal','stemmed' and 'stopped' for the get_queries_list(mode) function. If 'normal' is selected, the default queries are chosen for the run. If 'stopped' is chosen, queries go through stopping. If 'stemmed' is chosen, the stemmed queries are used. When mode 'stemmed' is chosen, mode must be 'stemmed' for the function set_index_corpus_path(mode), otherwise it should be set to 'normal'. This function will set the index and corpus path accordingly. The output of this file will be the following two:<br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  a) A text file under the same name containing the top 100 results for each of the 64 queries along with the score.<br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  b) A pickle file of a dictionary where key is a query and value is the list of all ranked documents.<br />
        
iii) BM25.py - This file requires the relevance information and so relevance.py must be run to generate the pickle file before running this code. This query function in this code has only two settings: 'normal' and 'stopped'. If 'normal' is selected, the default queries are chosen for the run. If 'stopped' is chosen, queries go through stopping. Stemming isn't included as there isn't any relevance information for the stemmed queries. This function will set the index and corpus path accordingly. The output of this file will be the following two:<br />
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; a) A text file under the same name containing the top 100 results for each of the 64 queries along with the score.<br />
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; b) A pickle file of a dictionary where key is a query and value is the list of all ranked documents.<br />

The ranking from Lucene is found using the following two files in Java:<br />

1)IndexFiles.java: The code was found on a Lucene tutorial <http://lucene.apache.org/core/8_0_0/demo/src-html/org/apache/lucene/demo/IndexFiles.html>. This file when run on Eclipse will index all the raw HTML files and store them in the specified directory. We have to specify the path to the raw HTML files to the variable  'String docsPath'. We also have to include the path to the location where we want to store the indexed documents on our computer in the variable 'String indexPath'.<br />

2)SearchFiles.java: The code was found on a Lucene tutorial <http://lucene.apache.org/core/8_0_0/demo/src-html/org/apache/lucene/demo/SearchFiles.html>. This file should be in the same directory as the IndexFiles.java. This file when run on Eclipse will prompt the user to enter a query. It will print the top 100 documents matching the query ranked in the order of decreasing relevance per page.<br />

The results from Lucene were stored in a text file manually. This text file was then parsed using the file 'lucene.py' to form a pickle file similar to the ones generated by other models containing the ranking.<br />
 
 Query Expansion:<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;There are two methods of query expansion:<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i)Pseudorelevance feedback - This is implemented with the code in 'pseudorelevance_feedback.py'. This code requires the pickle file relevance.pickle as it takes relevance judgements into consideration. This code will take ranking dictionary pickle file generated from a retrievel model as input and generate a pickled queries dictionary where keys are the query id and value is the query with expanded terms.<br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii)Thesaurus expansion - This is implemented with the code in 'thesaurusExpansion.py'. This code will take ranking dictionary pickle file generated from a retrievel model as input and generate a pickled queries dictionary where keys are the query id and value is the query with expanded terms.<br />
        
When a retrievel model requires query enhancement, the results pickle file of a run has to be given as input to one of the above methods, and the generated output pickle file with expanded queries,i.e, the new queries input pickle should replace the existing queries pickle file in the retrievel model code.<br />

2.Displaying the results<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For displaying the results below two files have been used.<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. snippetGenerationWithHL.py - This code accepts list of documents, query and maximum snippet length as parameter. For the given query it iterates through fulltext of all the documents one by one, and for each full text it tries to find the snippet which has all/maximum number of terms with closest proximity.<br />
    
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. resultHTMLBuilder.py - This code generates a single html file for each of the 64 queries, containing snippets from top 100 documents ranked based on tf-idf score. It puts all the result html files in a single folder. The folder path needs to be changed to successfully run this code. This uses snippetGenerationWithHL.py file, thus the above file needs to be there to run this.<br />
  
3.Evaluation:<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The evaluation is done with just one file: evaluation.py. The input to this file is an array called 'runs'. Each item in the list is a tuple containing a dictionary generated from the above retrieval runs (containing the rankings in sorted order) and a name for the run. The stored pickle files have to be loaded into dictionaries for this. The code when run will generate the following:<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i) A spreadsheet for each run with the precision and recall values for the top 100 documents for   the 52 queries whose relevance information is provided. (so 9 sheets in this case)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ii) A single spreadsheet containing the the MAP and MRR values for all the runs.<br />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ii) A single spreadsheet containing the the P@5 and P@20 values for each query for all the runs.<br />
           
4.Spelling correction - <br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For spelling correction below file is used:<br />
    spelling_correction.py - This file performs spelling correction. The input is a query string, consisiting of one or more terms. It checks every term and if there is a mistake, makes the correction with 6 alternatives. The output of this code is stored as a pickle file. It contains a dictionary where key is the incorrect query term and value is the six alternatives. Before this code is run, the auxillary code 'tokens_frequency.py' must be run. This will pickle a dictionary containing the frequencies of each word in the entire collection. 


## Libraries used
urllib.request, nltk, Beautiful soup, httplib2, collections, numpy, itertools, string, re, os, matplotlib.pyplot

##Development/IDEs
Eclipse(4.0 or above)

## Installation
 
This project requires Python 3.5 and Java 8.0. It also requires Lucene 8.0 which can be downloaded from <https://lucene.apache.org/core/downloads.html>.
There are a few python packages which have to be installed to be able to run the code. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them as follows:

```bash
pip install beautifulsoup4
pip install nltk
pip install collections
pip install beautifulsoup4
pip install nltk
pip install collections
pip install gensim
pip install pickle
pip install csv

```
## Usage

```bash
python corpus_generator.py 
python unigram_indexer.py
python relevance.py 
python generate_stemmed_corpus.py
python BM25.py
python tfidf.py
python QMD.py
python evaluation.py
```
The following steps have to be followed for snippet generation:

## Usage

```bash
python snippetGenerationWithHL.py
python resultHTMLBuilder.py
```

For Lucene:

Run IndexFiles.java (after modifying paths) followed by SearchFiles.java in Eclipse. Enter the query term to retrieve the top 100 documents.
