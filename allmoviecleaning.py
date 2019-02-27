
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


# In[153]:


path="E:\Crawledmovies\*.txt"

files = glob.glob(path)
titlelist=[]
summarylist=[]
ratinglist=[]
counter = 0
for file in files:
    counter += 1
    print(counter)
    myfile=open(file, 'r',encoding="utf8")
    data=myfile.read().replace('\n', ' ').replace('\t', ' ').replace(';',',') # Excel splits columns on ; by default, so this prevents that
    data = re.sub('\s+', ' ', data).strip() #replace sequences of spaces by single space
    data = html.unescape(data) #Decode html encoding
    title = re.search('<meta name="title" content="(.*) - ', data).group(1)
    if title is None:
        continue #jump to next file: If there is no title, we ignore the file
    else:
        titlelist.append(title)
        summary=re.search('<div class="text" itemprop="description">(.*)</section>', data)
        if summary is None:
            summarylist.append('')
        else:
            summary=summary.group(1).split('Characteristics')[0].strip() #Remove trailing non-summary text
            summarylist.append(summary)
    rating=re.search('rating-allmovie-(.*)"', data)
    rating=rating.group(1).split('"')[0].strip()
    if rating is None:
        ratinglist.append('None')
    elif rating =="0":             
        ratinglist.append("1")
    else:
        ratinglist.append(rating)


# In[154]:


#Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
summaryclean=[]
for my_str in summarylist:
	rest=re.sub('<.*?>', '', my_str)
	summaryclean.append(rest)


# In[165]:


#extract year for a column in df
yearlist=[]
for line in titlelist:
	title = re.search('\((\d+)\)', line)
	if title is None:
		yearlist.append('')
	else:
		title=title.group(1)
		yearlist.append(title)


# In[156]:


sep = '('
titlelistclean=[]
for x in titlelist:
	rest = x.split(sep, 1)[0].split(' - ')[0].strip()
	titlelistclean.append(rest)


# In[167]:


data = pd.DataFrame({'title': titlelistclean, 'summary': summaryclean,"year":yearlist,"allmovierating":ratinglist})


# In[168]:


data


# In[149]:


data.to_csv("allmovieclean.csv", encoding='utf-8', index=False)

