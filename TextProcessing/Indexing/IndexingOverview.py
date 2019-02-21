# first basic Indexer

# structure of dictionary:
# key = term
# values are:
#   -Frequency
#   -In which documents it occurs
#   -weight for each doc (initialize all the same), tf-idf could be implemented later
#   -tf per document
#   -term position, a list per document

# keys = stemmed term, 5 values are freq, pointers to docs, weight per doc, tf per doc, term pos in doc
IndexDictionary = {}

# create main function that allows for MultiProcessing.

# function =  input: list of csv('s), number of instances. Output: x (equal to number of instances) amount of batchDictionaries.

# Seperate batch file function:

# function: to parse csv files
    # every line in a csv represents a page
    # every line will be processed by the following three functions:

# function = input: string with text. outputs: list of cleaned tokens
    # indexable text: lowercase, tokenize, remove white space and punctuation, remove stop words, convert terms to their stems

# function = input: pointer to MovieObject, list with cleaned tokens. Output: make dict with unique terms with values a list of indexes places in the original list 
    # intermediate dict, together in a list with the pointer
    # MovieObject with a key existing of (no spaces or non-alphanumerical characters) title_year: contains information of all different sites

# function = input: list with pointer and intermediate dict. Output: parse the terms in the dict and place them in the BatchDictionary, can be save as a file 
    # Batchdict



# Finally: indexing has to be done distributed. First implementation will be that batches will be made, run seperately and then be combined.

# function = input: list of BatchDictionary(ies). Output: join values into IndexDictionary




#questions
#   -what do we do with document meta data? so title and year. wanna throw this in the index as well. Do we make another dict?
#   => goes into the MovieObject
#   -