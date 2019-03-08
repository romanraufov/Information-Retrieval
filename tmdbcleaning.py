
# coding: utf-8

# In[2]:



import numpy as np
import pandas as pd
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


# In[29]:


path="E:\Crawledmovies\*.txt"
files = glob.glob(path)

titlelist=[]
summarylist=[]
yearlist = []
tmdbscorelist=[]


for file in files:
    myfile = open(file, 'r',encoding="utf8")
    soup = BeautifulSoup(myfile.read(), "html.parser")
    title = soup.find("meta", property="og:title")['content']#.split("(")
    summary = soup.find('meta', attrs={"name": "description"})['content']#.split(">")
    summary = summary.lower()
    year=soup.find('span', {'class': 'release_date'}).contents[0]
    tmdb=soup.find('div', {'class': 'user_score_chart'})['data-percent']

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
        if tmdb is None:
            tmdbscorelist.append('')
        else:
            tmdbscorelist.append(tmdb)


# In[38]:


yearlistclean=[]
for line in yearlist:
    title=re.search(r'\((.*?)\)',line).group(1)
    if title is None:
        pass
    else:
        yearlistclean.append(title)




# In[39]:


data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlistclean,"tmdb":tmdbscorelist})
data.to_csv("tmdbclean.csv", encoding='utf-8', index=False)

