
# coding: utf-8

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
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 


base_path = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\Multicrawler"
#hier path naar txt files


#Debugging
#path= base_path + "\\rottentomatoes\\*.txt"

#all files
path = "C:\\Users\\chris\\OneDrive\\Documenten\\DataScience\\InformationRetrieval\\ScrapedSites\\RottenTomatoes\\*.txt"
path = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\Multicrawler\\multisitestoreNew\\*.txt"

files = glob.glob(path)
#print(files)


titlelist=[]
summarylist=[]
yearlist = []
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
		summary = soup.find("meta", property="og:description")['content']
	except:
		summary = ""

	#print(title, ":  ", summary)

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

	if counter % int(totalFileCount/20) == 0:
		print("Cleaning data at {}%".format((math.ceil((counter/totalFileCount)*100))))

#print("titlelist: ", titlelist)
#print("summarylist: ", summarylist)

# #Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
# summaryclean=[]
# for my_str in summarylist:
# 	rest=re.sub('<.*?>', '', my_str)
# 	summaryclean.append(rest)

# #extract year for a column in df
# yearlist=[]
# for line in titlelist:
# 	title = re.search('\((\d+)\)', line)
# 	if title is None:
# 		yearlist.append('')
# 	else:
# 		title=title.group(1)
# 		yearlist.append(title)

# #Clean the title for the dataframe
# sep = '('
# titlelistclean=[]
# for x in titlelist:
# 	rest = x.split(sep, 1)[0].split(' - |')[0].strip()
# 	titlelistclean.append(rest)

  
#data = pd.DataFrame({'title': titlelistclean, 'summary': summaryclean,"year":yearlist})
data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist})

#print(data)
#data["title"]
data.to_csv("C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessed\\RottenTomatoesNew.csv", index=False, quoting=csv.QUOTE_ALL)
print("\n RottemTomatoes files have been cleaned")