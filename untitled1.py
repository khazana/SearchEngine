#!/usr/bin/env python3
from bs4 import BeautifulSoup

fh = open('/Users/fathimakhazana/Documents/IRFinalProject/cacm/CACM-0001.txt',"r")
contents = fh.read()
soup = BeautifulSoup(contents,"html.parser")
text = soup.text
print(text)


tokens_string = fh.read()
list1 = [x.strip() for x in tokens_string.split(',')]