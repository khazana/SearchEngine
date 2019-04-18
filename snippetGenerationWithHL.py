import re
import copy
from operator import itemgetter


def extractSnippetFromFulltext(fulltext,qterms,maxSnippetLength):
    listOfIndices = []
    lengthlist = []
    i = 0

    for element in qterms:
        lengthlist.append(len(element))
        singleIndexList = []
        for match in re.finditer(element, fulltext):
            listOfIndices.append({"Start":match.start(),"TermNum":i})
        i = i + 1

    listOfIndices = sorted(listOfIndices, key=itemgetter('Start')) 

    finallist = []
    tempList = []

    def findLength(entries):
        listOfPos = []
        for entry in entries:
            listOfPos.append(entry["Start"])

        difference = max(listOfPos) - min(listOfPos)
        return difference

    minDifference = 0

    for listel in listOfIndices:
        TermNum = listel["TermNum"]
        Found = False
        for entry in finallist:
            if(entry["TermNum"] == TermNum):
                Found = True
                tempList = copy.copy(finallist)
                tempList[tempList.index(entry)] = listel
                lengthAfterChange = findLength(tempList)
                if(lengthAfterChange==0 or lengthAfterChange < minDifference):
                    finallist = copy.copy(tempList)
                    minDifference = findLength(tempList)
                break

        if(not Found):
            finallist.append(listel)
            minDifference = findLength(finallist)

    finallist  = sorted(finallist, key = itemgetter('Start'))
    finalel = finallist[-1]
    firstel = finallist[0]
    Start = firstel["Start"]

    End = finalel["Start"] + lengthlist[finalel["TermNum"]] - 1

    finalSnippet = ""

    if(len(fulltext) < maxSnippetLength):
        Start = 0
        finalSnippet = fulltext
        End = len(fulltext)
    else:
        if(End - Start + 1 )< maxSnippetLength:
            paddingLen = int((maxSnippetLength - (End-Start))/2)

            Start = Start - paddingLen + 1
            End = End + paddingLen + 1
            
            if(Start <= 0):
                End = End + (0-Start)
                Start = 0
            if(End >= len(fulltext)):
                Start = Start - (len(fulltext) - End)
                End = len(fulltext)

            finalSnippet = fulltext[Start:End]
        else:
            End = Start + maxSnippetLength
            finalSnippet = fulltext[Start:End]

    listOfHLStarts = []

    for element in qterms:
        for match in re.finditer(element,finalSnippet):
            listOfHLStarts.append({"Start":(Start) + match.start(), "End":(Start) + match.end()})

    listOfHLStarts = sorted(listOfHLStarts, key = itemgetter('Start'))

    finalSnippetWithHL = ""


    startPos = Start

    if(startPos != 0):
        finalSnippetWithHL = "..."

    for entry in listOfHLStarts:
        finalSnippetWithHL = finalSnippetWithHL + fulltext[startPos:entry["Start"]]
        finalSnippetWithHL = finalSnippetWithHL + "<b>" + fulltext[entry["Start"]:entry["End"]]+ "</b>"
        startPos = entry["End"]

    finalSnippetWithHL = finalSnippetWithHL + fulltext[startPos:End]

    if(startPos<(len(fulltext)-1)):
        finalSnippetWithHL = finalSnippetWithHL + "..."

    
    return finalSnippetWithHL
