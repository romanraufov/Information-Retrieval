
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
tmdbscorelist=[]
tmdburllist=[]
watchtypelist = []
counter = 0

totalFileCount = len(files)
for file in files:
	#print("file: ", file)
	counter += 1
	myfile = open(file, 'r',encoding="utf8")
	soup = BeautifulSoup(myfile.read(), "html.parser")
	
	title = soup.find("meta", property="og:title")['content'].strip()
	year = soup.find("span", {"class":"release_date"}).text.split('(')[1].split(')').strip()
	tmdbscore = soup.find("div", {"class":"user_score_chart"})['data-percent']
	
	summary = soup.find("meta", property="og:description")['content']
	summary = summary.lower().split(".")
	if len(summary) == 1:
		summary = summary[0]
	elif "ted by" in summary[0]:
		summary = summary[1:]
	if "with" in summary[0][:10]:
		summary = summary[1:]
		summary = ".".join(summary)

	watchtype = soup.find("meta",  {"prpperty":"og:type"})['content']
	if not watchtype:
		watchtype = ["Movie"]
		
	tmdburl=soup.find("meta", property="og:url")['content'].split("/>")
	if title is None:
		continue #jump to next file: If there is no title, we ignore the file
	else:
		titlelist.append(title)
		watchtypelist.append(watchtype)
		if summary is None:
			summarylist.append('')
		else:
			summarylist.append(summary)
		if year is None:
			yearlist.append('')
		else:
			yearlist.append(year)
		if tmdburl is None:
			tmdburllist.append('')
		else:
			tmdburllist.append(imdburl)


data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist, "type":watchtypelist,"tmdbscore":tmdbscorelist,"tmdburl":tmdburllist})
data.to_csv("tmdb.csv", encoding='utf-8', index=False, quoting=csv.QUOTE_ALL)

