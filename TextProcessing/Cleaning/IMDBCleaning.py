
# coding: utf-8

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
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 


base_path = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\Multicrawler"
#hier path naar txt files


#Debugging
path= base_path + "\\imdb\\*.txt"

#all files
#path = "C:\\Users\\chris\\OneDrive\\Documenten\\DataScience\\InformationRetrieval\\ScrapedSites\\RottenTomatoes\\*.txt"

files = glob.glob(path)
#print(files)


titlelist=[]
summarylist=[]
yearlist = []
WatchTypelist = []
counter = 0
WatchTypePosibilities = ["Episode", "Video", "Series"]

totalFileCount = len(files)
for file in files:
	#print("file: ", file)
	counter += 1
	myfile = open(file, 'r',encoding="utf8")
	soup = BeautifulSoup(myfile.read(), "html.parser")
	#print(soup)
	#print("tags: ", soup.find("meta", property="og:title")['content'])
	metaTag = soup.find("meta", property="og:title")['content'].split("(")
	CurrentWatchType = [i for i in WatchTypePosibilities if i in metaTag[-1]]
	if not CurrentWatchType:
		CurrentWatchType = ["Movie"]
	title = metaTag[:-1][0]
	#print(title)
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
		WatchTypelist.append(CurrentWatchType[0])

	if counter == 200:
		break

	if counter % int(totalFileCount/20) == 0:
		print("Cleaning data at {}%".format((math.ceil((counter/totalFileCount)*100))))


# #print("titlelist: ", titlelist)
# #print("summarylist: ", summarylist)

# # #Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
# # summaryclean=[]
# # for my_str in summarylist:
# # 	rest=re.sub('<.*?>', '', my_str)
# # 	summaryclean.append(rest)

# # #extract year for a column in df
# # yearlist=[]
# # for line in titlelist:
# # 	title = re.search('\((\d+)\)', line)
# # 	if title is None:
# # 		yearlist.append('')
# # 	else:
# # 		title=title.group(1)
# # 		yearlist.append(title)

# # #Clean the title for the dataframe
# # sep = '('
# # titlelistclean=[]
# # for x in titlelist:
# # 	rest = x.split(sep, 1)[0].split(' - |')[0].strip()
# # 	titlelistclean.append(rest)

  
# #data = pd.DataFrame({'title': titlelistclean, 'summary': summaryclean,"year":yearlist})
print("saving csv")
data = pd.DataFrame({'title': titlelist, 'summary': summarylist,"year":yearlist, "type":WatchTypelist})
data.to_csv("C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessed\\imdb.csv", index=False, quoting=csv.QUOTE_ALL)

print("\n RottemTomatoes files have been cleaned")