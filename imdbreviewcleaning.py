
# coding: utf-8

# In[2]:


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


# In[24]:


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
    for x in soup.findAll("div", class_="text show-more__control"):
        templist.append(list(x))

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


# In[26]:


data = pd.DataFrame({'title': titlelist,"year":yearlist, "userreviews":reviews})
#data.to_csv("imdbclean.csv", encoding='utf-8', index=False)
data

