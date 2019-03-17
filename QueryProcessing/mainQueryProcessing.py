# global import
import pickle
import sys
import operator
from collections import Counter
from datetime import datetime

# local import
sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing')
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF
#######

# load dict
def getDict():
    path2dict = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\MainIndex_Complete_2019-03-17.pkl"
    pickle_in = open(path2dict,"rb")
    return pickle.load(pickle_in)

def getTitleDict():
    path2dict = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\TitleIndex_Complete_2019-03-17.pkl"
    pickle_in = open(path2dict,"rb")
    return pickle.load(pickle_in)

def SearchIndex(term, indexDict):
    try:
        termValue = indexDict[term]
    except:
        IMF.addTime("term not in Index")
        termValue = False
    return termValue

def retrieveWeights(termIndex):
    weightsTerm = [termIndex['pointers'], termIndex['weights']]
    return weightsTerm

def add2QueryDict(pointer, weight, queryDict):
    if pointer in queryDict:
        queryDict[pointer] += weight
    else:
        queryDict[pointer] = weight
    return queryDict

def buildQueryDict(query, IndexDict):
    """
    input: query and SearchIndexDictionary
    ouput: query dictionary containing documents and weights
    """
    queryDict = {}
    for term in query:
        termIndex = SearchIndex(term, IndexDict)
        if not termIndex:
            continue
        docsWeight = retrieveWeights(termIndex)
        for i in range(len(docsWeight[0])):
            queryDict = add2QueryDict(docsWeight[0][i], docsWeight[1][i], queryDict)
    return queryDict

def getTopDocs(resultDict, nReturned = 10):
    # TODO if nReturned == -1, return all docs
    # TODO what happens if the list is not long enough?
    addCounter = Counter(resultDict)
    TopDocs = addCounter.most_common(10)
    TopList = [pair[0] for pair in TopDocs]
    return(TopList)

IndexDict = getDict()
def ProcessQuery(query):
    cQuery = IF.cleanText(query)
    resultDict = buildQueryDict(cQuery, IndexDict)
    topDocs = getTopDocs(resultDict)
    return topDocs

IndexTitleDict = getTitleDict()
def ProcessTitleQuery(query):
    cQuery = IF.cleanText(query)
    resultDict = buildQueryDict(cQuery, IndexTitleDict)
    topDocs = getTopDocs(resultDict)
    return topDocs

def mainProcessor(query):
    summaryIndex = ProcessQuery(query)
    titleIndex = ProcessTitleQuery(query)
    sumOnly = [x for x in summaryIndex if x not in titleIndex]
    topRank = titleIndex + sumOnly
    return topRank


# Query Processing Executers

def interactiveSearch():
    searchQuery = 'start'
    while searchQuery:
        # query processing
        searchQuery = input("\nenter your search query: ")
        if searchQuery == 'quit':
            break
        TimeAtBeginning = datetime.now()
        foundDocs = mainProcessor(searchQuery)
        TimeAtEnd = datetime.now()

        #show result
        IMF.addTime("\nThese are the found documents on your query: " + searchQuery + "\n")
        for doc in foundDocs:
            print(doc)
        print("\n")
        IMF.addTime("search time is: {:.5f} seconds".format((TimeAtEnd-TimeAtBeginning).total_seconds()))

def automatedTestSearch():
    testList = getTestList()
    TimeAtBeginning = datetime.now()
    DocsPerQuery = {}
    for query in testList:
        DocsPerQuery[query] = ProcessQuery(query)
    TimeAtEnd = datetime.now()

    IMF.addTime("These documents have been for the following queries: \n")
    for query in DocsPerQuery:
        print(query, "- found docs: ",DocsPerQuery[query])
    IMF.addTime("search of all {} queries executed in {:.5f} seconds".format(len(testList) ,(TimeAtEnd-TimeAtBeginning).total_seconds()))
    IMF.addTime("average search time of {:.5f} seconds".format((TimeAtEnd-TimeAtBeginning).total_seconds()/len(testList)))

def getTestList():
    # TODO: load a big external testList
    testList = ["Pirates of the Caribbean","Monty Python", "A star is Born", "The Terminator", "Little Miss Sunshine", "The Matrix"]
    return testList


#interactiveSearch()
#automatedTestSearch()