# global import
import pickle
import sys
import math

# local import
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF
import IndexingMultiple as IM
#######


# load dict
def getDict():
    path2dict = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\NewIndex_2019-02-28V2.pkl"
    pickle_in = open(path2dict,"rb")
    return pickle.load(pickle_in)

# save dict
def saveNewDict(WeightDict):
    path2save = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\"
    fullPath = path2save + "NewBatchWeightedIndex"
    IF.saveDict(WeightDict, fullPath, ".pkl")
    IMF.addTime("Dictionary with weights has been saved in folder: \n" + path2save)

# get weights per documents by tf-idf way
def addWeights2Dict(IndexDict):
    dictCounter = 0
    lenghtDict = len(IndexDict)
    TotalDocs = getTotalDocsInCorpus()
    for term in IndexDict:
        documentFreq = IndexDict[term]["documentFrequency"]
        termFreqencies = IndexDict[term]["termFrequencies"]
        for termFreq in termFreqencies:
            IndexDict[term]["weights"].append(getWeightValue(TotalDocs, termFreq, documentFreq))
        dictCounter += 1
        if dictCounter % math.ceil(lenghtDict/5) == 0:
            IMF.addTime("weighting at {}%".format((math.ceil((dictCounter/lenghtDict)*100))))
    IMF.addTime("weighting complete")
    return IndexDict

# helper functions
def getWeightValue(TotDocs, termFreq, docFreq):
    idf = getIDF(TotDocs, docFreq)
    rawTF_IDF = termFreq * idf
    roundTF_IDF = round(rawTF_IDF,5)
    return roundTF_IDF

def getIDF(TotDocs, docFreq):
    return math.log10(TotDocs / docFreq)

def getTotalDocsInCorpus():
    try:
        path2csv = IM.getMainMovieCSV()
        numberDocs = IMF.getCSVLength(path2csv)
    except:
        numberDocs = 70000
    return numberDocs


IndexDict = getDict()
DictWithWeights = addWeights2Dict(IndexDict)
saveNewDict(DictWithWeights)

