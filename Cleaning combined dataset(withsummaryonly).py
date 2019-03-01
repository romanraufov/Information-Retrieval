
# coding: utf-8

# In[ ]:


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
import unicodedata
get_ipython().run_line_magic('matplotlib', 'inline')
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 



# In[ ]:


df = pd.read_csv('combined_data.csv', sep=',')


# In[ ]:
def strip_accents(text):

   
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

df=df[(df["summary"].str.len()>6)]
df['summary'] = df['summary'].replace('"','', regex=True)
df['summary'] = df['summary'].apply(lambda x: x.lower())
df['summary'] = df['summary'].str.replace('[^\w\s]','')
df['summary'] = df['summary'].str.replace('\r', '')
df['summary'] = df['summary'].str.replace('\n', '')
df['summary'] = df['summary'].str.replace('&#246;', 'e')
df['summary'] = df['summary'].str.replace('&#233;', 'e')
df['summary'] = df['summary'].str.replace('&#235;', 'e')
df['summary'] = df['summary'].str.replace('&#8364;', '')
df['summary'] = df['summary'].str.replace('&#239;', 'i')
df['summary'] = df['summary'].str.replace('&#8226;', 'i')
df['summary'] = df['summary'].str.replace('&apos;', '')
df['summary'] = df['summary'].str.replace('#215;', '/')
df['summary'] = df['summary'].str.replace('&amp;', '')
df['summary'] = df['summary'].str.replace('&#8230;', '')
df['summary'] = df['summary'].str.replace('&apos;', '')
df['summary'] = df['summary'].str.replace('&#225;', '')
df['summary'] = df['summary'].str.replace('&quot;', '')


df['summary'] = df['summary'].map(lambda x: strip_accents(str(x)))
df['summary'] = df['summary'].map(lambda x: re.sub(r'[^\x00-\x7F]+',' ', str(x)))


df.to_csv("combineddataCLEAN.csv", encoding='utf-8', index=False)

