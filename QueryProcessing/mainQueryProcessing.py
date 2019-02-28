# global import
import pickle
import sys
import operator
from collections import Counter

# local import
sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing')
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF
#######



# load dict
def getDict():
    path2dict = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\FullWeightedIndex_2019-02-28.pkl"
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
    addCounter = Counter(resultDict)
    TopDocs = addCounter.most_common(10)
    TopList = [pair[0] for pair in TopDocs]
    return(TopList)

#Testing
IndexDict = getDict()
IMF.addTime(IndexDict['consfront'])
IMF.addTime(SearchIndex('consfront', IndexDict))

IndexDict = getDict()
def ProcessQuery(query):
    cQuery = IF.cleanText(TestQuery)
    resultDict = buildQueryDict(cQuery, IndexDict)
    topDocs = getTopDocs(resultDict)
    return topDocs

TestQuery = "Pirate of the Caribbean"
foundDocs = ProcessQuery(TestQuery)
IMF.addTime(foundDocs)
