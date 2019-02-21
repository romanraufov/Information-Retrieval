# functions for the indexer
#######
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# function return pointerName
def getKeyName(title, year):
    pattern = re.compile('[\W_]+')
    titleClean = pattern.sub('', title.lower())
    KeyName = titleClean + "_" + year
    return KeyName

# function = input: string with text. outputs: list of cleaned tokens
# indexable text: lowercase, tokenize, remove white space and punctuation, remove stop words, convert terms to their stems
def cleanText(SummaryString):
    pattern = re.compile('[\W_]+')
    CleanSummary = pattern.sub(' ', SummaryString.lower())
    #print(CleanSummary)
    # function = RemoveStopWords
    tokenized = word_tokenize(CleanSummary) # tokenize
    stopwordsRemoved = stopWordRemover(tokenized) # remove stopwords
    listStemmed = stemmer(stopwordsRemoved) # stem terms
    return listStemmed

# helpfunctions for cleanText
ps = PorterStemmer()
def stemmer(listOfTerms):
    stemmed = [ps.stem(term) for term in listOfTerms]
    return stemmed
stop_words = set(stopwords.words('english')) 
def stopWordRemover(listOfTerms):
    filteredList = [term for term in listOfTerms if not term in stop_words] 
    return filteredList




# function = input: pointer to MovieObject, list with cleaned tokens. Output: make dict with unique terms with values a list of indexes places in the original list 
    # intermediate dict, together in a list with the pointer
    # MovieObject with a key existing of (no spaces or non-alphanumerical characters) title_year: contains information of all different sites

# function = input: list with pointer and intermediate dict. Output: parse the terms in the dict and place them in the BatchDictionary, can be save as a file 
    # Batchdict



# Testing KeyName
# getKeyNameTest = ["Hello! World :)", "1992"]
# getKeyName(getKeyNameTest[0], getKeyNameTest[1])


# Testing Text Cleaner
# testSum = "a seemingly indestructible android is sent from 2029 to 1984 to assassinate a waitress, whose unborn son will lead humanity in a war against the machines, while a soldier from that war is sent to protect her at all costs.fox, christopher lloyd, lea thompson, crispin glover. marty mcfly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling delorean invented by his close friend, the maverick scientist doc brown. rocky balboa proudly holds the world heavyweight boxing championship, but a new challenger has stepped forward: drago, a six-foot-four, 261-pound fighter who has the backing of the soviet union."
# cleanText(testSum)



