
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


path="D:\\RTCrawler\\rottentomatoes\\*.txt"

files = glob.glob(path)
titlelist=[]
summarylist=[]
yearlist = []
tomatometerlist = []
audiencescorelist = []
audienceratinglist = []
criticsratinglist = []
counter = 0
totalFileCount = len(files)
print("starting up cleaning process..")
for file in files[:100]:
	counter += 1
	myfile=open(file, 'r',encoding="utf8")
	file_text = myfile.read()
	soup = BeautifulSoup(file_text, "html.parser")
	#print("tags: ", soup.find("meta", property="og:title")['content'][-5:-1])
	metaTag = soup.find("meta", property="og:title")['content']
	title = metaTag[:-7]
	year = metaTag[-5:-1]
	try:
		summary = soup.find("meta", property="og:description")['content'].replace('"','')#.split(">")
	except:
		summary = ""
	#try:
	scores = soup.findAll("h1", {"id":"tomato_meter_link"})
	tomatometer_score = scores[0].text.strip()
	audience_score = scores[1].text.strip()
	audience_avg_rating = soup.findAll("span", {"id":"js-rotten-count"})[1].text.strip()
	critics_avg_rating = file_text.split('"tomatometerAllCritics":{"avgScore":')[1].split(',')[0].strip()
	"""
	except:
		tomatometer_score = 'No score available'
		audience_score = 'No score available'
		audience_avg_rating = 'No rating available'
		critics_avg_rating = 'No rating available'
	"""
	tomatometerlist.append(tomatometer_score)
	audiencescorelist.append(audience_score)
	audienceratinglist.append(audience_avg_rating)
	criticsratinglist.append(critics_avg_rating)
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


# In[87]:


data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist,"tomatometer":tomatometerlist,"audience score":audiencescorelist,"average audience rating":audienceratinglist,"average critics rating":criticsratinglist})
data.to_csv("RottenTomatoes.csv", index=False, quoting=csv.QUOTE_ALL)


# In[29]:


#data.to_csv("rottentomatoes.csv", encoding='utf-8', index=False)

