# global import
import pickle
import sys

# local import
sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing')
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF
#######



# load dict
path2dict = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\SavedIndexes\\FullIndexes\\FullFirstIndex_2019-02-22.pkl"

pickle_in = open(path2dict,"rb")
IndexDict = pickle.load(pickle_in)


TestQuery = "Pirate of the Caribbean"

# clean query
cQuery = IF.cleanText(TestQuery)
IMF.addTime(cQuery)

# build query dict
    # initialize empty dict
        # empty dict in which docs are added with weight value
    # per term:
        # retrieve documents
        # enumerate docs and weights file
        # doc is not in query dict:
            # create doc-key and weight-value
        # doc is in query dict:
            # sum weight to weight in dict
    # return query dict

# sort query dict
    # return list with docs in rank order

# get top documents
    # return list of n top documents





#Testing
IndexDict.keys()
IMF.addTime(IndexDict['consfront'])
