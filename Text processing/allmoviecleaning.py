
# coding: utf-8

# In[430]:


import pandas as pd
import numpy as np 
import matplotlib as plt
import seaborn as sns
import glob , numpy
import os.path
import re
import html
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 


# In[456]:


#hier path naar txt files
path="C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie\\*.txt"
files = glob.glob(path)
titlelist=[]
summarylist=[]
for file in files:
	myfile=open(file, 'r',encoding="utf8")
	data=myfile.read().replace('\n', ' ').replace('\t', ' ')
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
			summary=summary.group(1)
			summarylist.append(summary)


# In[432]:


#Need to clean summaries, this is as clean as it gets. Still need normalize and stem ofc
summaryclean=[]
for my_str in summarylist:
	rest=re.sub('<.*?>', '', my_str)
	summaryclean.append(rest)




# In[434]:


#extract year for a column in df
yearlist=[]
for line in titlelist:
	title = re.search('\((\d+)\)', line)
	if title is None:
		yearlist.append('')
	else:
		title=title.group(1)
		yearlist.append(title)


# In[435]:


#Clean the title for the dataframe
sep = '('
titlelistclean=[]
for x in titlelist:
	rest = x.split(sep, 1)[0].split(' -  |')[0].strip()
	titlelistclean.append(rest)

    


# In[436]:

data = pd.DataFrame({'title': titlelistclean, 'summary': summaryclean,"year":yearlist})

# In[344]:


data.to_csv("flixable.csv", encoding='cp1252', index=False)

