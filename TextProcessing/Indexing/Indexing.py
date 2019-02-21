# Global Imports
import glob
import numpy as np
import pandas as pd
import math


# Local Imports
import IndexerFunctions as IF


# Main Index Dictionary
IndexDictionary = {}

# Load list of CSV files containing info for indexing
path2csvs = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessed\\*.csv"
csvfiles = glob.glob(path2csvs)

# input: list of csvs. output: oneMain DF.
def csv2DF(listofCsv):
    ListOfPD = [pd.read_csv(csv) for csv in listofCsv] # load files
    for i in range(len(listofCsv)): 
        ListOfPD[i]['domain'] = listofCsv[i].split("\\")[-1].split(".")[0] # add source to rows
    MainPD = pd.concat(ListOfPD, sort=True) # concat to one big df
    return MainPD

#input: batch DF. output: BatchDict
def Indexer(BatchDF):
    #execute function per row
    batchDict = {}
    for index, row in BatchDF.iterrows():
        #print("\n next title: ", row["title"])
        try: 
            KeyName = IF.getKeyName(row["title"], str(row["year"]))
            listOfTerms = IF.cleanText(row["title"] + str(row["summary"]))
        except:
            print("fail due to Something")
            print("title: ", row["title"])
            print("year: ", row["year"])
            print("summary: ", row["summary"])
            continue
        #F: return intermediate dict
        intermediateDict = IF.getUniqueTerms(listOfTerms)
        #F: return BatchDict
        batchDict = IF.add2BatchDict(batchDict, intermediateDict, KeyName)
        #For testing
        #print(row['summary'])
        #print(KeyName)
        #print(listOfTerms)
        #print(intermediateDict)
        #print(batchDict["small"])
    return batchDict

def mergeBatchInMainIndex(IndexDictionary, batchDict):
    for batchKey in batchDict:
        if batchKey not in IndexDictionary:
            IndexDictionary[batchKey] = batchDict[batchKey]
        else:
            IndexDictionary[batchKey]['pointers'] = IndexDictionary[batchKey]['pointers'] + batchDict[batchKey]['pointers']
            IndexDictionary[batchKey]['termFrequencies'] = IndexDictionary[batchKey]['termFrequencies'] + batchDict[batchKey]['termFrequencies']
            IndexDictionary[batchKey]['termPositions'] = IndexDictionary[batchKey]['termPositions'] + batchDict[batchKey]['termPositions']
            IndexDictionary = IF.updateDocFreq(IndexDictionary, batchKey)
            IndexDictionary = IF.updateWeightsTerm(IndexDictionary, batchKey)
    print("batch has been merged to the main Index")
    return IndexDictionary



mainPF = csv2DF(csvfiles)
print(mainPF)

# Testing in batches
#IndexBatch1 = mainPF.iloc[:20]
# IndexBatch2 = mainPF.iloc[20:40]
# IndexBatch3 = mainPF.iloc[40:100]

# batchIndex1 = Indexer(IndexBatch1)
# batchIndex2 = Indexer(IndexBatch2)
# batchIndex3 = Indexer(IndexBatch3)

# batchIndex1["small"]
# batchIndex2["small"]
# batchIndex3["small"]

# IndexDictionary = mergeBatchInMainIndex(IndexDictionary, batchIndex1)
# IndexDictionary = mergeBatchInMainIndex(IndexDictionary, batchIndex2)
# IndexDictionary = mergeBatchInMainIndex(IndexDictionary, batchIndex3)
# IndexDictionary["small"]



# Testing all
IndexBatchAll = mainPF
batchIndexAll = Indexer(IndexBatchAll)
IndexDictionary = mergeBatchInMainIndex(IndexDictionary, batchIndexAll)
IndexDictionary["small"]

IF.saveDict(IndexDictionary, "testIndex", ".pkl")
