import os
from string import punctuation
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
import nltk

def remove_punctuations(content):
    content = ''.join(characters for characters in content if characters not in '!}{][)(\><=#"$%&,/*`\'')
    punc = punctuation.replace('-',"")
    content = ' '.join(token.strip(punc) for token in content.split() if token.strip(punc))
    content = ' '.join(token.replace("'", "") for token in content.split() if token.replace("'", ""))
    content = ' '.join(content.split())
    return content


def format_content(bsObj, casefolding = True, removepunc = True):
    result = BeautifulSoup(bsObj, 'lxml').get_text()
    result = ' '.join(result.split())
    result = result.replace('html ', '')
    result = ''.join(content for content in result if 0 < ord(content) < 127)
    if casefolding:
        result = result.lower()  # case folding
    if removepunc:
        result = remove_punctuations(result)
    return result


def set_parameters():
    html_cleaner = Cleaner()
    html_cleaner.javascript = True
    html_cleaner.comments = True
    html_cleaner.scripts = True
    html_cleaner.meta = True
    html_cleaner.links = True
    html_cleaner.embedded = True
    html_cleaner.frames = True
    html_cleaner.forms = True
    html_cleaner.style = True
    html_cleaner.remove_unknown_tags = True
    html_cleaner.processing_instructions = True
    html_cleaner.annoying_tags = True
    html_cleaner.remove_tags = ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'span', 'b', 'a', 'u', 'i', 'body']
    html_cleaner.kill_tags = ['script', 'noscript', 'style', 'meta', 'semantics', 'img', 'label', 'table', 'li', 'ul',
                   'ol', 'nav', 'dl', 'dd', 'sub', 'sup', 'math']
    return html_cleaner


def get_cleaned_content(filename, crawled_files_location):
    cleaner = set_parameters()
    with open(crawled_files_location + filename,  'rb') as f:
        bsObj = BeautifulSoup(f.read(), 'html.parser')
        f.close()
        bsObj = cleaner.clean_html(str(bsObj.find('pre')))
        formatted_content = format_content(bsObj)
    return formatted_content


def main():
    crawled_files_path = "/Users/fathimakhazana/Documents/IRFinalProject/cacm/"
    corpus_path = "/Users/fathimakhazana/Documents/IRFinalProject/ParsedFiles/"


    for name in os.listdir(crawled_files_path):
        clean_data = get_cleaned_content(name, crawled_files_path)
        clean_data = nltk.tokenize.word_tokenize(clean_data)
        with open(corpus_path+name.split(".")[0]+".txt", 'w') as f:
            for item in clean_data:
                f.write("%s\n" % item)


if __name__ == "__main__":
    main()
