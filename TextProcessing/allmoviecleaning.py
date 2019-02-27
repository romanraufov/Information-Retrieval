
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
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 


base_path = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\Multicrawler"
#hier path naar txt files
path= base_path + "\\allmovie\\*.txt"

files = glob.glob(path)
titlelist=[]
summarylist=[]
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

#Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
summaryclean=[]
for my_str in summarylist:
	rest=re.sub('<.*?>', '', my_str)
	summaryclean.append(rest)

#extract year for a column in df
yearlist=[]
for line in titlelist:
	title = re.search('\((\d+)\)', line)
	if title is None:
		yearlist.append('')
	else:
		title=title.group(1)
		yearlist.append(title)

#Clean the title for the dataframe
sep = '('
titlelistclean=[]
for x in titlelist:
	rest = x.split(sep, 1)[0].split(' - |')[0].strip()
	titlelistclean.append(rest)

  
data = pd.DataFrame({'title': titlelistclean, 'summary': summaryclean,"year":yearlist})


data.to_csv("flixable.csv", encoding='cp1252', index=False)
print("Allmovie files have been cleaned")
