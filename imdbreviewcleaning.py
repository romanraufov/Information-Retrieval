
# coding: utf-8

# In[1]:


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

from bs4 import BeautifulSoup


# In[6]:


path="E:\Crawledmovies\*.txt"
files = glob.glob(path)

titlelist=[]
yearlist = []
WatchTypelist = []
imdburllist=[]
reviews=[]
counter = 0
WatchTypePosibilities = ["Episode", "Video", "Series"]

totalFileCount = len(files)
for file in files:
    #print("file: ", file)
    counter += 1
    myfile = open(file, 'r',encoding="utf8")
    soup = BeautifulSoup(myfile.read(), "html.parser")
    #print("tags: ", soup.find("meta", property="og:title")['content'])
    metaTag = soup.find("meta", property="og:title")['content'].split("(")
    CurrentWatchType = [i for i in WatchTypePosibilities if i in metaTag[-1]]
    if not CurrentWatchType:
        CurrentWatchType = ["Movie"]
    title = metaTag[:-1][0]
    yearpart = re.findall('\d+', metaTag[-1])
    year = yearpart[0] if len(yearpart) == 1 else yearpart[0] + "-" + yearpart[1]
    imdburl=soup.find("meta", property="og:url")['content'].split("/>")
    #review=soup.find("div", class_="text show-more__control")['content']

    div class="text show-more__control"
    if title is None:
        continue #jump to next file: If there is no title, we ignore the file
    else:
        titlelist.append(title)
        if year is None:
            yearlist.append('')
        else:
            yearlist.append(year)
            WatchTypelist.append(CurrentWatchType[0])
        if imdburl is None:
            imdburllist.append('')
        else:
            imdburllist.append(imdburl)
        #if review is None:
        #    reviews.append("")
        #else:
         #   reviews.append(review)


# In[12]:


reviews=[]
path="E:\Crawledmovies\*.txt"
files = glob.glob(path)
for file in files:
        myfile=open(file, 'r',encoding="utf8")
        data=myfile.read().replace('\n', ' ').replace('\t', ' ').replace(';',',')
        imdb=re.search('<div class="text show-more__control">(.*)<div class="actions text-muted">', data)
        if imdb is None:
            reviews.append('')
        else:
            imdb=imdb.group(1).split('</div')[0].strip()
            reviews.append(imdb)


# In[16]:


len(reviews)


# In[3]:


imdburllistclean=[val for sublist in imdburllist for val in sublist]


# In[5]:


data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist, "type":WatchTypelist,"imdburl":imdburllistclean})
#data.to_csv("imdbclean.csv", encoding='utf-8', index=False)
data

