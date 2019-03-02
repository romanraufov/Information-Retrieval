# global import
import pickle
import sys
import operator
from collections import Counter

# local import
sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing')

# local imports
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF
import IndexTerms2beRemoved as ITR
import IndexWeights as IW

# open as dictionaries:
def getMainDict():
    mainIndex = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\mainIndexTestUpdate_2019-03-02.pkl"
    mainIndex = IMF.getDict(mainIndex)
    return mainIndex

def getNewDict():
    newIndex = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\newIndexTestUpdate_2019-03-02.pkl"
    newIndex = IMF.getDict(newIndex)
    return newIndex

def mergeIndexes(mainIndex, newIndex):
    indictCount = 0 # testing
    for newTerm in newIndex:
        if newTerm not in mainIndex:
            mainIndex[newTerm] = newIndex[newTerm]
        else:
            indictCount += 1
            if indictCount > 11:
                for i in range(len(newIndex[newTerm]['pointers'])):
                    if newIndex[newTerm]['pointers'][i] in mainIndex[newTerm]['pointers']: #update old
                        j = mainIndex[newTerm]['pointers'].index(newIndex[newTerm]['pointers'][i])
                        mainIndex[newTerm]['pointers'][j] = newIndex[newTerm]['pointers'][i]
                        mainIndex[newTerm]['termFrequencies'][j] = newIndex[newTerm]['termFrequencies'][i]
                        mainIndex[newTerm]['termPositions'][j] = newIndex[newTerm]['termPositions'][i]
                    else: # add new
                        mainIndex[newTerm]['pointers'].append(newIndex[newTerm]['pointers'][i])
                        mainIndex[newTerm]['termFrequencies'].append(newIndex[newTerm]['termFrequencies'][i])
                        mainIndex[newTerm]['termPositions'].append(newIndex[newTerm]['termPositions'][i])
    return mainIndex

# Issue: when a document used to have a term that does not have it any more, it is still in the index. How to resolve this?
def removeTerms(mainIndex, list2Remove):
    docPointers = list2Remove.keys()
    for docPointer in docPointers:
        for term in list2Remove[docPointer]:
            i = mainIndex[term]["pointers"].index(docPointer)
            del mainIndex[term]["pointers"][i]
            del mainIndex[term]["termFrequencies"][i]
            del mainIndex[term]["termPositions"][i]
        return mainIndex

# takes input path to MovieObject csv, new and old
def getPath2Main():
    path2Main = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessedTest\\mainTest.csv"
    return path2Main

def getPath2New():
    path2New = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessedTest\\newTest.csv"
    return path2New

# recalculate frequencies
def updateFreq(mainIndex):
    for key in mainIndex:
        mainIndex = IF.updateDocFreq(mainIndex, key)
    return mainIndex

def indexUpdateMain():
    # merge dicts
    mainIndex = getMainDict()
    newIndex = getNewDict()
    mainIndex = mergeIndexes(mainIndex, newIndex)
    # get list of items to be removed
    path2Main = getPath2Main()
    path2New = getPath2New()
    getTerm2Remove = ITR.getTermsToBeRemoved(path2Main, path2New)
    #remove unused terms
    mainIndex = removeTerms(mainIndex, getTerm2Remove)
    #update frequencies
    mainIndex = updateFreq(mainIndex)
    #update weights
    mainIndex = IW.addWeights2Dict(mainIndex)

    # save new mainIndex

    path2MainIndex = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\"
    IF.saveDict(mainIndex, path2MainIndex + "TestIndexAfterUpdate", ".pkl")

indexUpdateMain()



