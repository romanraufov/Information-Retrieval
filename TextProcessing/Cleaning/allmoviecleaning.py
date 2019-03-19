
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
from bs4 import BeautifulSoup
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 


base_path = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\Multicrawler"
#hier path naar txt files
path="C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie\\*.txt"
files = glob.glob(path)
titlelist=[]
cleantitlelist=[]
yearlist=[]
summarylist=[]
ratinglist=[]
urllist=[]
counter = 0
for file in files:
	counter += 1
	print(counter)
	myfile=open(file, 'r',encoding="utf8")
	soup = BeautifulSoup(myfile.read(), "html.parser")
	#try:
	try:
		rating = soup.find("div", {"class":"allmovie-rating"}).text.strip()
	except:
		rating = 'No rating available'
	if rating == '':
		rating = 'No rating available'
			
	data=myfile.read().replace('\n', ' ').replace('\t', ' ').replace(';',',') # Excel splits columns on ; by default, so this prevents that
	data = re.sub('\s+', ' ', data).strip() #replace sequences of spaces by single space
	data = html.unescape(data) #Decode html encoding
	titletag = ''
	title = ''
	year = ''
	titletag = soup.find("meta", {"name":"title"})['content']
	if '(' in titletag:
		title = titletag.split('(')[0].strip()
		year = re.search('\((\d+)\)', titletag).group(1)
	else:
		title = titletag.split('-  |')[0].strip()
	url = soup.find("meta", {"property":"og:url"})['content']
	try:
		summary= soup.find("div",{"itemprop":"description"}).text.split('Characteristics')[0].strip() #re.search('<div class="text" itemprop="description">(.*)</section>', data)
	except:
		summary = ''
	titlelist.append(title)
	cleantitlelist.append(re.sub(r'[^a-zA-Z0-9_]','',str(title).strip()).lower()+'_'+str(year))
	yearlist.append(year)
	ratinglist.append(rating)
	summarylist.append(summary)
	urllist.append(url)
	#except:
	#	print("failed for "+file)
	#	continue

#Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
summaryclean=[]
for my_str in summarylist:
	rest=re.sub('<.*?>', '', my_str)
	summaryclean.append(rest)

  
data = pd.DataFrame({'title': titlelist,'cleantitle':cleantitlelist, 'summary': summaryclean,"year":yearlist, 'rating':ratinglist,'AllMovieUrl':urllist})


data.to_csv("AllMovie.csv", encoding='utf-8', index=False)
print("Allmovie files have been cleaned")
