# functions for the indexer
#######
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from collections import Counter
import datetime
import pickle
import os  

# function return pointerName
def getKeyName(title, year):
    pattern = re.compile('[\W_]+')
    titleClean = pattern.sub('', title.lower())
    KeyName = titleClean + "_" + year
    return KeyName

# function = input: string with text. outputs: list of cleaned tokens
# indexable text: lowercase, tokenize, remove white space and punctuation, remove stop words, convert terms to their stems
def cleanText(SummaryString):
    CleanSummary = normalizeSentence(SummaryString)
    #print(CleanSummary)
    # function = RemoveStopWords
    tokenized = word_tokenize(CleanSummary) # tokenize
    stopwordsRemoved = stopWordRemover(tokenized) # remove stopwords
    listStemmed = stemmer(stopwordsRemoved) # stem terms
    return listStemmed

# helpfunctions for cleanText
def normalizeSentence(dirtyString):
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', dirtyString.lower())
ps = PorterStemmer()
def stemmer(listOfTerms):
    stemmed = [ps.stem(term) for term in listOfTerms]
    return stemmed
stop_words = set(stopwords.words('english')) 
def stopWordRemover(listOfTerms):
    filteredList = [term for term in listOfTerms if not term in stop_words] 
    return filteredList


# function = input: pointer to MovieObject. Output: make dict with unique terms with values a list of indexes places in the original list 
    # intermediate dict, together in a list with the pointer
    # MovieObject with a key existing of (no spaces or non-alphanumerical characters) title_year: contains information of all different sites

def getUniqueTerms(listOfTerms):
    pageDict = {}
    UniqueTerms = list(set(listOfTerms))
    for uniqueTerm in UniqueTerms:
        pageDict[uniqueTerm] = [i for i, term in enumerate(listOfTerms) if term == uniqueTerm]
    return pageDict


# function = input: list with pointer and intermediate dict. Output: parse the terms in the dict and place them in the BatchDictionary, can be save as a file 
    # Batchdict
def add2BatchDict(batchDict, intermediateDict, pagePointer):
    # for keys in intermediateDict
    for term in intermediateDict:
        if not term in batchDict:
            batchDict[term] = initializeTermDict()
        batchDict[term]["pointers"].append(pagePointer)
        batchDict[term]["termFrequencies"].append(len(intermediateDict[term]))
        batchDict[term]["termPositions"].append(intermediateDict[term])
        batchDict = updateDocFreq(batchDict, term)
        #TODO: implement weight function
        batchDict = updateWeightsTerm(batchDict, term)
    # update term weight
    return batchDict
    
# BatchDict helper functions:
def initializeTermDict():
    return {"documentFrequency":0, "pointers":[] ,"weights":[] ,"termFrequencies":[] ,"termPositions":[]}
def updateDocFreq(batchDict, term):
    batchDict[term]["documentFrequency"] = len(batchDict[term]["pointers"]) 
    return batchDict
def updateWeightsTerm(batchDict, term):
    #TODO:implement weight
    #batchDict[term][weights] = 
    return batchDict


# Utilities
def saveDict(obj, name, ext):
    filePath = legitFilePath(name, ext)
    with open(filePath, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def legitFilePath(filename, ext):
    dateStamp = datetime.datetime.today().strftime('%Y-%m-%d')
    if not os.path.isfile(filename + "_" + dateStamp + ext):
        return filename + "_" + dateStamp + ext
    else:
        counter = 1
        while os.path.isfile(filename + "_" + dateStamp + "V" + str(counter) + ext):
            counter +=1
        print("saved as file: ", filename + "_" + dateStamp + "V" + str(counter) + ext)
        return filename + "_" + dateStamp + "V" + str(counter) + ext





# Testing KeyName
# getKeyNameTest = ["Hello! World :)", "1992"]
# getKeyName(getKeyNameTest[0], getKeyNameTest[1])


# Testing Text Cleaner
# testSum = "a seemingly indestructible android is sent from 2029 to 1984 to assassinate a waitress, whose unborn son will lead humanity in a war against the machines, while a soldier from that war is sent to protect her at all costs.fox, christopher lloyd, lea thompson, crispin glover. marty mcfly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling delorean invented by his close friend, the maverick scientist doc brown. rocky balboa proudly holds the world heavyweight boxing championship, but a new challenger has stepped forward: drago, a six-foot-four, 261-pound fighter who has the backing of the soviet union."
# cleanText(testSum)

# Testing UniqueTerm retriever
testTerms = ['seemingli', 'indestruct', 'android', 'sent', '2029', '1984', 'assassin', 'waitress', 'whose', 'unborn', 'son', 'lead', 'human', 'war', 'machin', 'soldier', 'war', 'sent', 'protect', 'cost', 'fox', 'christoph', 'lloyd', 'lea', 'thompson', 'crispin', 'glover', 'marti', 'mcfli', '17', 'year', 'old', 'high', 'school', 'student', 'accident', 'sent', 'thirti', 'year', 'past', 'time', 'travel', 'delorean', 'invent', 'close', 'friend', 'maverick', 'scientist', 'doc', 'brown', 'rocki', 'balboa', 'proudli', 'hold', 'world', 'heavyweight', 'box', 'championship', 'new', 'challeng', 'step', 'forward', 'drago', 'six', 'foot', 'four', '261', 'pound', 'fighter', 'back', 'soviet', 'union']
TestUniqueTerms = getUniqueTerms(testTerms)
TestUniqueTerms['sent']

# Testing dict
testDict = initializeTermDict()
testDict

