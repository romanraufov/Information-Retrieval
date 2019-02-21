# Global Imports
import glob
import numpy as np
import pandas as pd

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
    for index, row in BatchDF.iterrows():
        print("\n next title: ", row["title"])
        KeyName = IF.getKeyName(row["title"], row["year"]) # compose MovieObject Name
        listOfTerms = IF.cleanText(row["title"] + row["summary"]) # cleans text and puts it into list of terms. Note that title is added to this
        #F: return intermediate dict


        #F: return BatchDict

        #return BatchDict


        #For testing
        #print(row['summary'])
        #print(KeyName)
        print(listOfTerms)

        




mainPF = csv2DF(csvfiles)
print(mainPF)

IndexBatch = mainPF.iloc[:20]

Indexer(IndexBatch)
