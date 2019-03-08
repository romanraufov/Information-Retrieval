
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np 
import matplotlib as plt
import seaborn as sns
import glob , numpy
import os
import os.path
import re
import html
import csv
import math
import unicodedata
import nltk


import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


# In[32]:


### SCHOONMAKEN!!!!!!#############
def strip_accents(text):


    text = unicodedata.normalize('NFD', text)           .encode('ascii', 'ignore')           .decode("utf-8")

    return str(text)


def clean(review):
    #try:
        #review = review.apply(lambda x: x.lower())
    review = review.replace('[^\w\s]','')
    review = review.replace('\r', '')
    review = review.replace('\n', '')
    review = review.replace('&#246;', 'e')
    review = review.replace('&#233;', 'e')
    review = review.replace('&#235;', 'e')
    review = review.replace('&#8364;', '')
    review = review.replace('&#239;', 'i')
    review = review.replace('&#8226;', 'i')
    review = review.replace('&apos;', '')
    review = review.replace('#215;', '/')
    review = review.replace('&amp;', '')
    review = review.replace('&#8230;', '')
    review = review.replace('&apos;', '')
    review = review.replace('&#225;', '')
    review = review.replace('&quot;', '')


    review = strip_accents(review)
    return review
    #except:
    #    return ""


# In[37]:


#### INSERT HERE LOAD CSV WITH LIST OF LISTS REVIEWS PER MOVIE
path="E:\Crawledmovies\*.txt"
files = glob.glob(path)

titlelist=[]
yearlist = []
imdburllist=[]
reviews=[]

totalFileCount = len(files)
for file in files:
    templist=[]
    #print("file: ", file)
    myfile = open(file, 'r',encoding="utf8")
    soup = BeautifulSoup(myfile.read(), "html.parser")
    #print("tags: ", soup.find("meta", property="og:title")['content'])
    metaTag = soup.find("meta", property="og:title")['content'].split("(")
    title = metaTag[:-1][0]
    yearpart = re.findall('\d+', metaTag[-1])
    year = yearpart[0] if len(yearpart) == 1 else yearpart[0] + "-" + yearpart[1]
    for x in soup.findAll("div", class_="text show-more__control")[:50]:
        x=clean(x.text)
        templist.append([x])

    if title is None:
        continue #jump to next file: If there is no title, we ignore the file
    else:
        titlelist.append(title)
        if year is None:
            yearlist.append('')
        else:
            yearlist.append(year)
        if templist is None:
            reviews.append("")
        else:
            reviews.append(templist)


# In[38]:


data = pd.DataFrame({'title': titlelist,"year":yearlist, "summary":reviews})
#data.to_csv("imdbclean.csv", encoding='utf-8', index=False)
data


# In[39]:


#### FROM HERE REAL SENTIMENT ANALYSIS CODE######################
nltk.download('popular')

# A function that extracts which words exist in a text based on a list of words to which we compare.
def word_feats(words):
        return dict([(word, True) for word in words])

# Get the negative reviews for movies    
negids = movie_reviews.fileids('neg')

# Get the positive reviews for movies
posids = movie_reviews.fileids('pos')
 
# Find the features that most correspond to negative reviews    
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]

# Find the features that most correspond to positive reviews
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# We would only use 1500 instances to train on. The quarter of the reviews left is for testing purposes.
negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)


# In[40]:


# Construct the training dataset containing 50% positive reviews and 50% negative reviews
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]

# Construct the negative dataset containing 50% positive reviews and 50% negative reviews
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

print ('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

# Train a NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(trainfeats)

# Test the trained classifier and display the most informative features.
print ('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
classifier.show_most_informative_features()

def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict


# In[41]:


finallist=[]
for movie in data["summary"]:
    templist=[]
    for x in movie:
        words = word_tokenize(str(x))
        words = create_word_features(words)
        output=classifier.classify(words)
        templist.append(output)
    finallist.append(templist)     
  
data["sentiment"]=finallist


# In[42]:


data

