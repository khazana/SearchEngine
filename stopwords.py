
def getStopWordslist():
    with open('./common_words.txt', 'r') as f:
        stop_words = f.readlines()
    
    for i in range(0,len(stop_words)):
        stop_words[i] = stop_words[i].strip().lower()
    
    return stop_words

def remStopWords(text):
    words = text.split()
    stop_words = getStopWordslist()
    finaltext = ""

    for r in words: 
        if not r.lower() in stop_words: 
            finaltext  = finaltext + " " + r

    return finaltext

