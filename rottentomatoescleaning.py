
# coding: utf-8

# In[22]:


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


# In[86]:


path="E:\Crawledmovies\*.txt"

files = glob.glob(path)
titlelist=[]
summarylist=[]
yearlist = []
rtscorelist=[]
counter = 0
totalFileCount = len(files)
print("starting up cleaning process..")
for file in files:
	counter += 1
	myfile=open(file, 'r',encoding="utf8")
	soup = BeautifulSoup(myfile.read(), "html.parser")
	#print("tags: ", soup.find("meta", property="og:title")['content'][-5:-1])
	metaTag = soup.find("meta", property="og:title")['content']
	title = metaTag[:-7]
	year = metaTag[-5:-1]
	try:
		summary = soup.find("meta", property="og:description")['content']#.split(">")
	except:
		summary = ""
	try:
		score=int(min(soup.find('span', {'class': 'meter-value superPageFontColor'}).contents[0]))#.split(">")
	except:
		score = ""
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
		if score is None:
			rtscorelist.append('')
		else:
			rtscorelist.append(score)            


# In[87]:


data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist,"rtscore":rtscorelist})
data.to_csv("C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessed\\RottenTomatoes.csv", index=False, quoting=csv.QUOTE_ALL)


# In[29]:


data.to_csv("rottentomatoesclean.csv", encoding='utf-8', index=False)

