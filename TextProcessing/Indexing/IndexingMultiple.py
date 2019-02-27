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
import IndexerFunctions as IF
import IndexingMachineFunctions as IMF


# Main Index Dictionary
IndexDictionary = {}

# Load list of CSV files containing info for indexing


def getMainMovieCSV():
	path2csvs = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessed\\*.csv"
	csvfiles = glob.glob(path2csvs)
	return csvfiles[0]

# not being used with only 1 file
# input: list of csvs. output: oneMain DF.
def csv2DF(listofCsv):
	ListOfPD = [pd.read_csv(csv) for csv in listofCsv] # load files
	for i in range(len(listofCsv)): 
		ListOfPD[i]['domain'] = listofCsv[i].split("\\")[-1].split(".")[0] # add source to rows
	MainPD = pd.concat(ListOfPD, sort=True) # concat to one big df
	return MainPD

#input: batch DF. output: BatchDict
def Indexer(BatchDF):
	# Indexing part
	batchDict = {}
	dfLength = len(BatchDF.index)
	for index, row in BatchDF.iterrows():
		#print("\n next title: ", row["title"])
		try: 
			KeyName = IF.getKeyName(row["title"], str(row["year"]))
			listOfTerms = IF.cleanText(row["title"] + str(row["combined_summaries"]))
		except:
			print("fail due to Something")
			print("title: ", row["title"])
			print("year: ", row["year"])
			print("combined_summaries: ", row["combined_summaries"])
			continue
		#F: return intermediate dict
		intermediateDict = IF.getUniqueTerms(listOfTerms)
		#F: return BatchDict
		batchDict = IF.add2BatchDict(batchDict, intermediateDict, KeyName)


		#For testing
		#print(row['combined_summaries'])
		#print(KeyName)
		#print(listOfTerms)
		#print(intermediateDict)
		#print(batchDict["small"])

		# following process of Indexing Machines
		if index % math.ceil(dfLength/5) == 0:
			print("Indexing at {}%".format((math.ceil((index/dfLength)*100))))
	#print("Indexing at {}%".format((math.ceil((index/dfLength)*100))))
	#print("Indexing complete")
	return batchDict

def IndexingMachine(MovieCSV, MovieCSVHeader , lengthMainCSV, IndexLogCSV, batchSize, process_id, access_lock):
	while True:
		#Communication phase with the shared stacks
		with access_lock.get_lock():
			IMF.addTime("access lock acquired by process " + process_id)
			# function = mainIndexHolder. retrieve last parsed line.
			startIndex = IMF.retrieveIndex(IndexLogCSV) # retrieve last Index in Indexlog
			if startIndex > lengthMainCSV:
				return
			endIndex = startIndex + batchSize
			IMF.updateIndex(IndexLogCSV, process_id, startIndex, endIndex, IMF.getTimeStamp()) # update IndexLog
			batchDF = IMF.getBatch(MovieCSV, MovieCSVHeader, startIndex, endIndex) # retrieve batch from CSV
		IMF.addTime("access lock released by process "+process_id)
		
		batchDictionary = Indexer(batchDF) # Index Batch
		# Save batch to pickle file
		batchDirectory = './MultipleIndexLogFiles/BatchIndexFiles/'
		IF.saveDict(batchDictionary, batchDirectory + "IndexMachine_" + process_id + "_BatchIndex", ".pkl")
		IMF.addTime("Process {} has completed a batch".format(process_id))

		IMF.addTime("Indexing at {}%".format((math.ceil((startIndex/lengthMainCSV)*100))))
		time.sleep(1)
	
def main(args):
	"""
	input: list containting: batchSize, numberOfProcesses
	"""
	TimeAtBeginning = datetime.now()
	access_lock = multiprocessing.Value('i', 0)
	batchSize = int(args[0])
	num_procs = int(args[1])   # Number of processes to create

	MovieCSV = getMainMovieCSV()
	MovieCSVHeader = IMF.getCSVHeader(MovieCSV)
	lengthMainCSV = IMF.getCSVLength(MovieCSV)
	
	IndexLogFile = IMF.createIndexLog()
	

	jobs = []
	for i in range(0, num_procs):
		process = multiprocessing.Process(target=IndexingMachine, 
										   args=(MovieCSV, MovieCSVHeader, lengthMainCSV, IndexLogFile, batchSize, str(i), access_lock))
		jobs.append(process)

	IMF.addTime("Index main csv file with {} Movie objects".format(lengthMainCSV))
	# Start the processes (i.e. calculate the random number lists)
	for j in jobs:
		j.start()

	# Ensure all of the processes have finished
	for j in jobs:
		j.join()
	IMF.addTime("Indexing complete")
	IMF.addTime("Continueing to merge batches")
	merge2MainIndex()
	IMF.addTime("End of Process")
	TimeAtEnd = datetime.now()
	IMF.addTime("Elapsed time is: {:.2f} minutes".format((TimeAtEnd-TimeAtBeginning).total_seconds()/60))

# This one has to be rewritten. Also better in a different script
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

def merge2MainIndex():
	IMF.addTime("Merging batchdictionaries")
	MainIndexDictionary = {}
	path2pkls = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\BatchIndexFiles\\*.pkl"
	pklFiles = glob.glob(path2pkls)
	for pkl in pklFiles:
		pickle_in = open(pkl,"rb")
		mergeBatchInMainIndex(MainIndexDictionary, pickle.load(pickle_in))
	path2MainIndex = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\Indexing\\MultipleIndexLogFiles\\MainIndexFile\\"
	IF.saveDict(MainIndexDictionary, path2MainIndex + "MainIndex", ".pkl")
	IMF.addTime("Merging Complete, MainIndex has been saved")

# input: batch size, number of parallel processes
if __name__ == "__main__":
	main(sys.argv[1:])

