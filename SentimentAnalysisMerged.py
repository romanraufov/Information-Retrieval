# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:36:54 2018

@author: chris
"""


# Import all the libraries required
import random
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
from descartes import PolygonPatch
from shapely.geometry import Polygon, MultiPolygon

import pymongo
from pymongo import MongoClient
from pprint import pprint

# This snippet downloads the most popular datasets for experimenting with NLTK functionalities.
import nltk
nltk.download('popular')

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import twitter_samples

#%%

import csv
with open('C:\\Users\\chris\\OneDrive\\Documenten\\DataScience\\FunfamentalsOfDataScience\\week3_werkcollege_notebooks\\training.1600000.processed.noemoticon.csv', 'rb') as csvfile:
    df_stanford = pd.read_csv(csvfile, delimiter=',', encoding='cp437')

df_stanford.rename(columns={df_stanford.columns[5]: "tweet" }, inplace=True)

#%%

# Exporting as csv
client = MongoClient()
db = client["Fundamentals_34"]
tweet_data = (db.sentimentAnalysed .find({}))

df = pd.DataFrame(list(tweet_data))
df.drop(['_id'], axis=1)
df.to_csv("C:\\Users\\chris\\OneDrive\\Documenten\\DataScience\\FunfamentalsOfDataScience\\week3_werkcollege_notebooks\\sentimentAnalysed.csv", index=False)


#%% 

#df['Consensus'] = np.where((df['Stanford_sentiment'] == df['Tweet_samples']) & (df['Stanford_sentiment'] == df['Movie_reviews'])
     #                , "Consensus", "No-Consensus")

consensus = []
Two_out_ofThree = []
for index, row in df.iterrows():
    sumAverage = 0
    if row['Stanford_sentiment'] == 'neg' and row['Tweet_samples'] == 'neg' and row['Movie_reviews'] == 'neg':
        con = 'consensus-negative'
    elif row['Stanford_sentiment'] == 'pos' and row['Tweet_samples'] == 'pos' and row['Movie_reviews'] == 'pos':
        con = 'consensus-positive'
    else:
        con = 'no-consensus'
    consensus.append(con)
    
    
    if row['Stanford_sentiment'] == 'pos':
        sumAverage = sumAverage + 1
    if row['Tweet_samples'] == 'pos':
        sumAverage = sumAverage + 1
    if row['Movie_reviews'] == 'pos':
        sumAverage = sumAverage + 1
    
    
    if sumAverage > 1:
        two_out_three = 'positive-2/3'
    else:
        two_out_three = 'negative-2/3'
    
    Two_out_ofThree.append(two_out_three)
    
    
df['best-of-three'] = Two_out_ofThree
df['Consensus'] = consensus





#%%

#print(df.groupby('Consensus').count())
#df['Consensus'].count()

print(df.groupby('sentiment').count())
df[['best-of-three']].count()



#%%

#Import the tweets

amountOfTweets = None

client = MongoClient()
db = client["Fundamentals_34"]

fieldsToSelect = { "_id": 1, "created_at": 1, "text": 1, "coordinates": 1, "place": 1 }
tweet_data = (db.preprocessedTweets.find({}).limit(amountOfTweets)) if amountOfTweets is not None else (db.preprocessedTweets.find({}))
    
df = pd.DataFrame(list(tweet_data))

df.head()

#%%
# defines the datasets

# A function that extracts which words exist in a text based on a list of words to which we compare.
def movie_review_word_feats(words):
        return dict([(word, True) for word in words])
# Same as above but adapted for the Twitter samples
def word_feats_twitter(words):
        return dict([(word, True) for word in words.split(" ")])

#%%

# Movie reviews dataset
#######################
# Get the negative reviews for movies    
negids = movie_reviews.fileids('neg')

# Get the positive reviews for movies
posids = movie_reviews.fileids('pos')
 
# Find the features that most correspond to negative reviews    
movie_review_negfeats = [(movie_review_word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]

# Find the features that most correspond to positive reviews
movie_review_posfeats = [(movie_review_word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# We would only use 1500 instances to train on. The quarter of the reviews left is for testing purposes.
movie_review_negcutoff = int(len(movie_review_negfeats)*3/4)
movie_review_poscutoff = int(len(movie_review_posfeats)*3/4)

# Twitter samples dataset
#########################
negTweets = twitter_samples.strings('negative_tweets.json')
posTweets = twitter_samples.strings('positive_tweets.json')

# put the words in the right format for the NaiveBayesClassifier
tweets_negfeats = [(word_feats_twitter(f), 'neg') for f in negTweets]
tweets_posfeats = [(word_feats_twitter(f), 'pos') for f in posTweets]

tweets_negcutoff = int(len(tweets_negfeats)*3/4)
tweets_poscutoff = int(len(tweets_posfeats)*3/4)

#%%
# Trains the movie_reviews based dataset
# Construct the training dataset containing 50% positive reviews and 50% negative reviews
movie_review_trainfeats = movie_review_negfeats[:movie_review_negcutoff] + movie_review_posfeats[:movie_review_poscutoff]

# Construct the negative dataset containing 50% positive reviews and 50% negative reviews
movie_review_testfeats = movie_review_negfeats[movie_review_negcutoff:] + movie_review_posfeats[movie_review_poscutoff:]

print ('train on %d instances, test on %d instances' % (len(movie_review_trainfeats), len(movie_review_testfeats)))

# Train a NaiveBayesClassifier
movie_review_classifier = NaiveBayesClassifier.train(movie_review_trainfeats)

# Test the trained movie_review_classifier and display the most informative features.

movie_review_classifier.show_most_informative_features()

#%%
print ('accuracy:', nltk.classify.util.accuracy(movie_review_classifier, movie_review_testfeats))
print ('accuracy on tweets testfeats:', nltk.classify.util.accuracy(movie_review_classifier, tweets_testfeats))
print ('accuracy on stanfordtestfeats:', nltk.classify.util.accuracy(movie_review_classifier, stanford_testfeats))


#%%
# Trains the Twitter Samples based dataset
# Construct the training dataset containing 50% positive reviews and 50% negative reviews
tweets_trainfeats = tweets_negfeats[:tweets_negcutoff] + tweets_posfeats[:tweets_poscutoff]

# Construct the negative dataset containing 50% positive reviews and 50% negative reviews
tweets_testfeats = tweets_negfeats[tweets_negcutoff:] + tweets_posfeats[tweets_poscutoff:]

print ('train on %d instances, test on %d instances' % (len(tweets_trainfeats), len(tweets_testfeats)))

# Train a NaiveBayesClassifier
tweets_classifier = NaiveBayesClassifier.train(tweets_trainfeats)

# Test the trained classifier and display the most informative features.
tweets_classifier.show_most_informative_features()

#%%

print ('accuracy:', nltk.classify.util.accuracy(tweets_classifier, tweets_testfeats))
print ('accuracy on movie_review testfeats:', nltk.classify.util.accuracy(tweets_classifier, movie_review_testfeats))
print ('accuracy on stanford testfeats:', nltk.classify.util.accuracy(tweets_classifier, stanford_testfeats))


#%%

stanfordNegativeTweets = df_stanford.loc[df_stanford['0']==0]['tweet']
stanfordPositiveTweets = df_stanford.loc[df_stanford['0']==4]['tweet']

stanford_negfeats = [(word_feats_twitter(f), 'neg') for f in stanfordNegativeTweets]
stanford_posfeats = [(word_feats_twitter(f), 'pos') for f in stanfordPositiveTweets]

stanford_negcutoff = int(len(stanford_negfeats)*3/4)
stanford_poscutoff = int(len(stanford_posfeats)*3/4)


stanford_trainfeats = stanford_negfeats[:stanford_negcutoff] + stanford_posfeats[:stanford_poscutoff]
stanford_testfeats = stanford_negfeats[stanford_negcutoff:] + stanford_posfeats[stanford_poscutoff:]

stanford_classifier = NaiveBayesClassifier.train(stanford_trainfeats)

print ('train on %d instances, test on %d instances' % (len(stanford_trainfeats), len(stanford_testfeats)))


# Test the trained classifier and display the most informative features.
stanford_classifier.show_most_informative_features()

#%%
print ('accuracy:', nltk.classify.util.accuracy(stanford_classifier, stanford_testfeats))
print ('accuracy on movie_reviewfeats:', nltk.classify.util.accuracy(stanford_classifier, movie_review_testfeats))
print ('accuracy on twitter_samplefeats:', nltk.classify.util.accuracy(stanford_classifier, tweets_testfeats))



#%%
numberpos = 0
for i in range(0,10000,1):
    #i = random.randint(0,10000)
    tweet = df.iloc[i]['text']
    sentiment = stanford_classifier.classify(word_feats_twitter(tweet))
    print("\nsentiment: ", sentiment)
    print("the tweet:  ", tweet)
    if sentiment == 'pos':
        numberpos += 1
print("number of positive tweets:  ", numberpos)


#%%

# Movie_reviews based Classifying (First Classifier)
####################################################

numberPos = 0
indexPosTweets = []
for i in range(0,amountOfTweets,1):
    tweet = df.iloc[i]['text']
    sentimentTweet = movie_review_classifier.classify(movie_review_word_feats(tweet))
    if sentimentTweet == 'pos':
        numberPos += 1
        indexPosTweets.append(i)
print(numberPos)
print(indexPosTweets)

#%%

# Twitter Samples based Classifying (Second Classifier)
#######################################################

numberPos = 0
indexPosTweets2 = []
for i in range(0, len(indexPosTweets),1):
    tweet = df.iloc[indexPosTweets[i]]['text']
    sentimentTweet = tweets_classifier.classify(word_feats_twitter(tweet))
    if sentimentTweet == 'pos':
        numberPos += 1
        indexPosTweets2.append(i)

#print(indexPosTweets2)
print(numberPos)

#%%

# Applies all classsifier on each tweet when it has been rated positive
def applyAllClassifiers(tweet):
    sentimentTweet = movie_review_classifier.classify(movie_review_word_feats(tweet))
    if sentimentTweet == 'pos':
        sentimentTweet = tweets_classifier.classify(word_feats_twitter(tweet))
        if sentimentTweet == 'pos':
            sentimentTweet = stanford_classifier.classify(word_feats_twitter(tweet))
    if sentimentTweet == 'pos':
        sentimentTweet = 'positive'
    else:
        sentimentTweet = 'negative'
    return sentimentTweet


#%%
    
# apply classifiers and store them in the database
df['sentiment'] = df['text'].apply(lambda x: applyAllClassifiers(x))
df['Movie_reviews'] = df['text'].apply(lambda x: movie_review_classifier.classify(movie_review_word_feats(x)))
df['Tweet_samples'] = df['text'].apply(lambda x: tweets_classifier.classify(word_feats_twitter(x)))
df['Stanford_sentiment'] = df['text'].apply(lambda x: stanford_classifier.classify(word_feats_twitter(x)))

df.head()

#%%
# Shows the positive:negative ratios for the classifiers on the dataset
print("All classifiers combined:\n", df['sentiment'].value_counts(True))
print("Movie_reviews classifier:\n", df['Movie_reviews'].value_counts(True))
print("Tweet_samples classifier:\n", df['Tweet_samples'].value_counts(True))
print("Stanford_sentiment classifier:\n", df['Stanford_sentiment'].value_counts(True))

#%%
df = df.drop(['_id'], axis=1)

#%%
data_json = json.loads(df.to_json(orient='records', date_format=None))
db.sentimentAnalysed.insert_many(data_json)

#%%

df.to_csv(orient='records', date_format=None)




