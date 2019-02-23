import pandas as pd
from time import gmtime, strftime
import os
import IndexerFunctions as IF
import glob
import csv
from datetime import datetime

import pytz
cet = pytz.timezone('CET')

# Initiate start file:
# CSV with header: process, startIndex, endIndex, startProcessTime

def addTime(printableValue):
    print(getTimeStamp() + "  " + str(printableValue))

def getTimeStamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# creates log csv file and return the path to it
def createIndexLog():
    df = pd.DataFrame(columns=['process','startProcessTime','startIndex','endIndex'])
    df.loc[0] = ['init', getTimeStamp(), 0, 0]
    absolutePath2File = IF.saveDF2CSV(df, "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\IndexLog\\" + "IndexLogger")
    return absolutePath2File

def removeFile(path2File):
    os.remove(path2File)
    addTime(path2File + "has been removed")

def retrieveIndex(path2File):
    IndexLogDF = pd.read_csv(path2File)
    lastLine = IndexLogDF.iloc[-1]
    return lastLine["endIndex"]

def updateIndex(path2File, process, startIndex, endIndex, timestamp):
    newRow = str(process) + "," + timestamp + "," + str(startIndex) + "," + str(endIndex)
    with open(path2File,'a') as fd:
        fd.write(newRow + "\n")
    fd.close()

def getBatch(MovieCSV, MovieCSVHeader, startIndex, endIndex):
    chunk = endIndex - startIndex
    chunkDF = pd.read_csv(MovieCSV , sep=',', names = MovieCSVHeader, skiprows = startIndex, chunksize = chunk)
    return chunkDF.get_chunk()

def getCSVHeader(csvFile):
    with open(csvFile, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
    f.close()
    return header

def getCSVLength(csvFile):
    with open(csvFile, "rb") as f:
        row_count = sum(1 for row in f)
    f.close()
    return row_count
    







# # Testing
# path2csvs = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessed\\*.csv"
# csvfiles = glob.glob(path2csvs)
# logFile = createIndexLog()

# testHeader = getCSVHeader(csvfiles[0])  


# TestStartIndex = retrieveIndex(logFile)
# TestEndIndex = TestStartIndex + 30
# TestProcess = -1
# TS = getTimeStamp()
# updateIndex(logFile, TestProcess, TestStartIndex, TestEndIndex, TS)

# TestBatch = getBatch(csvfiles[0], testHeader, TestStartIndex, TestEndIndex)
# TestBatch

# for index, row in TestBatch.iterrows():
#     print(row)


# removeFile(logFile)
# TestLength = getCSVLength(csvfiles[0])