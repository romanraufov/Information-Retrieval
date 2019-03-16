import pickle

# load MovieDict
def getMovieObjectsDict():
    path2dict = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\MovieObjectFile\\MovieObjects.pickle"
    pickle_in = open(path2dict,"rb")
    return pickle.load(pickle_in)

def SearchIndex(term, indexDict):
    print("pointers to MovieObjects",term)
    try:
        termValue = indexDict[term]
    except:
        print("term not in MovieObjects")
        termValue = False
    return termValue

def getMovieInfo(listOfPointers):
    movieList = []
    for pointer in listOfPointers:
        movieInfo = SearchIndex(pointer, MovieObjectsDict)
        if not movieInfo:
            continue
        movieList.append(movieInfo)
    return movieList

MovieObjectsDict = getMovieObjectsDict()
# movieTest = getMovieInfo(["theoutstandingwoman_2014", "beastmaster2throughtheportaloftime_1991"])
# movieTest