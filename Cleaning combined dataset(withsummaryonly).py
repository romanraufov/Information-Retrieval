
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
get_ipython().run_line_magic('matplotlib', 'inline')
#let op, als het niet werkt start dit in de anaconda notebook
#breek op elke comment, dus code tussen comments in een aparte cell. 



# In[ ]:


df = pd.read_csv('combined_data.csv', sep=',')


# In[ ]:


df=df[(df["summary"].str.len()>6)]
df['summary'] = df['summary'].replace('"','', regex=True)
df['summary'] = df['summary'].apply(lambda x: x.lower())
df['summary'] = df['summary'].str.replace('[^\w\s]','')
df.to_csv("combineddataCLEAN.csv", encoding='utf-8', index=False)

