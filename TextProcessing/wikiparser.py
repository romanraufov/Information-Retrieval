import pandas as pd
import csv
import numpy as np

with open ('wikimoviepages.txt', 'r') as file:
	text = file.read()
	sections = text.split('Hier begint een titel!')[1:]
	title_column = []
	year_column = []
	summary_column = []
	for section in sections:
		title = section.split('Hier eindigt een titel!')[0].strip()
		plot = ''
		if 'Plot\n' in section:
			plot = section.split('Plot\n')[1].split('\n\n')[0].replace('\n',' ')
		if 'film)' in title:
			title_column.append(title.split('(')[0])
			year_column.append(title.split('(')[1].split('film')[0].strip())
			summary_column.append(plot)
		elif '(' not in title:
			title_column.append(title)
			year_column.append('')
			summary_column.append(plot)
	print(len(title_column))
	print(len(year_column))
	print(len(summary_column))
	d = {'title':title_column, 'year':year_column,'summary':summary_column}
	df = pd.DataFrame(data=d)
	df.to_csv('wikidata.csv', index=None)