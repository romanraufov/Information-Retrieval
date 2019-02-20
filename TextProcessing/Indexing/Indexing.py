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

# function: to parse csv files
    # every line in a csv represents a page
    # every line will be processed by the following three functions:

# function = input: string with text. outputs: list of cleaned tokens
    # indexable text: lowercase, tokenize, remove white space and punctuation, remove stop words, convert terms to their stems

# function = input: pointer to document, list with cleaned tokens. Output: make dict with unique terms with values a list of indexes places in the original list 
    # intermediate dict, together in a list with the pointer

# function = input: list with pointer and intermediate dict. Output: parse the terms in the dict and place them in the IndexDictionary 
    # final dict


#questions
#   -what do we do with document meta data? so title and year. wanna throw this in the index as well. Do we make another dict?
#   -