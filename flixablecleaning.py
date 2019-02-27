
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np 
import matplotlib as plt
import seaborn as sns
import cv2 , glob , numpy , pdb
import os.path
import re
import html
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
get_ipython().run_line_magic('matplotlib', 'inline')
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 


# In[26]:


#hier path naar txt files
path="E:\Crawledmovies\*.txt"
files = glob.glob(path)
titlelist=[]
summarylist=[]
tmdblist=[]
imdburllist=[]
for file in files:
        myfile=open(file, 'r',encoding="utf8")
        data=myfile.read().replace('\n', ' ').replace('\t', ' ').replace(';',',')
        title = re.search('<meta property="og:title" content="(.*) - ', data)
        if title is None:
            pass
        else:
            title=title.group(1)
            titlelist.append(title)
        summary=re.search('<meta property="og:description" content="(.*)">', data)
        if summary is None:
            pass
        else:
            summary=summary.group(1)
            summary=summary.split('">')[0].strip()
            summary=html.unescape(summary)
            summarylist.append(summary)
        tmdb=re.search('<img class="tmdb-logo" src="/images/tmdb-blue.svg"><span>(.*)/10', data)
        if tmdb is None:
            tmdblist.append(" ")
        else:
            tmdb=tmdb.group(1)
            tmdblist.append(tmdb)
        imdb=re.search('data-style="p1"><a href="(.*)?', data)
        if imdb is None:
            imdburllist.append(" ")
        else:
            imdb=imdb.group(1)
            imdb=imdb.split('?')[0].strip()
            imdburllist.append(imdb)


# In[27]:


len(titlelist)


# In[28]:


len(summarylist)


# In[29]:


len(tmdblist)


# In[45]:


len(summaryclean)


# In[55]:


summaryclean[60]


# In[54]:


#Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
summaryclean=[]
for my_str in summarylist:
    #rest=re.sub('"', '', my_str)
    rest=re.sub(',','', my_str)
    rest=re.sub('Ã©','e',my_str)
    rest=re.sub('â€™','',my_str)
    rest=re.sub('Ã¡','a',my_str)
    rest=re.sub('&#039,', '', my_str)
    summaryclean.append(rest)


# In[34]:


#extract year for a column in df
yearlist=[]
for line in titlelist:
    title = re.search('\((\d+)\)', line)
    if title is None:
        pass
    else:
        title=title.group(1)
        yearlist.append(title)


# In[35]:


#Clean the title for the dataframe
sep = '('
titlelistclean=[]
for x in titlelist:
    rest = x.split(sep, 1)[0]
    rest =re.sub('&#039,', '', rest)
    titlelistclean.append(rest)

    


# In[36]:


tmdbclean=[]
sep = '/'
for x in tmdblist:
    rest = x.split(sep, 1)[0]
    tmdbclean.append(rest)


# In[56]:


data = pd.DataFrame({'title': titlelistclean, 'summary': summaryclean,"year":yearlist,"tmdb":tmdbclean,"imdburlflix":imdburllist})
data


# In[57]:


data.to_csv("flixableclean.csv", encoding='utf-8', index=False)


# In[14]:


#DOWNLOAD ALL THE URL's
path="E:\Crawledmovies\*.txt"
files = glob.glob(path)
urls=[]
for file in files:
        myfile=open(file, 'r',encoding="utf8")
        for line in myfile:
            url = re.search('<meta property="og:url" content=(.*)>', line)
            if url is None:
                pass
            else:
                url=url.group(1)
                print(url)
                urls.append(url)
with open('urls.txt', 'w') as f:
    for item in urls:
        f.write("%s\n" % item)

