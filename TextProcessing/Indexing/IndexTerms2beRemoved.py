# Global Imports
import glob
import numpy as np
import pandas as pd
import math
import multiprocessing
import sys
import time
import pickle
from datetime import datetime

# Local Imports

sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing')
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF



#Load MainMovieObjectCSV into df
#Load newMovieObjectCSV into df

path2Main = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessedBackUp\\mainTest.csv"
path2New = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessedBackUp\\newTest.csv"

def getTermsToBeRemoved(path2Main, path2New):
    mainDF = pd.read_csv(path2Main)
    newDF = pd.read_csv(path2New)
    listCommonTitles = np.intersect1d(mainDF["cleantitle"], newDF["cleantitle"])
    docs2Remove = {}
    for commonTitle in listCommonTitles:
        summaryMain = mainDF.loc[mainDF['cleantitle'] == commonTitle, "combined_summaries"].iloc[0]
        summaryNew = newDF.loc[mainDF['cleantitle'] == commonTitle, "combined_summaries"].iloc[0]
        uniqueTermsMain = set(IF.cleanText(summaryMain))
        uniqueTermsNew = set(IF.cleanText(summaryNew))
        termsNotInMain = list(uniqueTermsMain - uniqueTermsNew)
        docs2Remove[commonTitle] = termsNotInMain
    return docs2Remove

#getTermsToBeRemoved(path2Main, path2New)
