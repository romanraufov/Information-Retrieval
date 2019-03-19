
# coding: utf-8

# In[51]:


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


# In[62]:


path="E:\Crawledmovies\*.txt"
files = glob.glob(path)

titlelist=[]
summarylist=[]
yearlist = []
WatchTypelist = []
imdburllist=[]
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
    summary = soup.find("meta", property="og:description")['content']

    summary = summary.lower().split(".")
    if len(summary) == 1:
        summary = summary[0]
    elif "ted by" in summary[0]:
        summary = summary[1:]
    if "with" in summary[0][:10]:
        summary = summary[1:]
        summary = ".".join(summary)
    imdburl=soup.find("meta", property="og:url")['content'].split("/>")
    if title is None:
        continue #jump to next file: If there is no title, we ignore the file
    else:
        titlelist.append(title)
        if summary is None:
            summarylist.append('')
        else:
            summarylist.append(summary)
        if year is None:
            yearlist.append('')
        else:
            yearlist.append(year)
            WatchTypelist.append(CurrentWatchType[0])
        if imdburl is None:
            imdburllist.append('')
        else:
            imdburllist.append(imdburl)


# In[76]:


imdblist=[]
path="E:\Crawledmovies\*.txt"
files = glob.glob(path)
for file in files:
        myfile=open(file, 'r',encoding="utf8")
        data=myfile.read().replace('\n', ' ').replace('\t', ' ').replace(';',',')
        imdb=re.search('itemprop="ratingValue">(.*)</span>', data)
        if imdb is None:
            imdblist.append('')
        else:
            imdb=imdb.group(1).split('<')[0].strip()
            imdblist.append(imdb)


# In[77]:


imdburllistclean=[]
for list1 in imdburllist:
    for my_str in list1:
        imdburllistclean.append(my_str)


# In[78]:


data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist, "type":WatchTypelist,"imdb":imdblist,"imdburl":imdburllistclean})
#data.to_csv("imdbclean.csv", encoding='utf-8', index=False)
data


# In[75]:


imdburllist

