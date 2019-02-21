import csv
import pandas
import os
import re
wikititles = []
imdbtitles = []
flixabletitles = []
rottentomatoestitles = []
combined_titles = []
allmovietitles = []
title_converter = {}
year_converter = {}
summary_converter = {}
for file in os.listdir(os.getcwd()):
	if '.csv' in file and 'combined' not in file:
		if 'allmovie' in file:
			#continue
			df = pandas.read_csv(file, encoding='cp1252')
		else:
			df = pandas.read_csv(file)
		titles = list(df['title'])
		summaries = df['summary']
		bare_cleantitles = [re.sub(r'[^a-zA-Z0-9_]','',str(title).strip()).lower() for title in titles]
		years = list(df['year'])
		cleantitles = [bare_cleantitles[i]+'_'+str(years[i]) for i in range(len(titles))]
		df['cleantitle']= cleantitles
		for i in range(len(titles)):
			title_converter[cleantitles[i]] = titles[i]
			if 'wiki' in file:
				if cleantitles[i] not in year_converter:
					if years[i] is not '0' and years[i] is not 0 and years[i] is not '' and years[i] is not 'nan':
						year_converter[cleantitles[i]] = years[i]
					else:
						year_converter[cleantitles[i]] = 'unknown'
			else:
				year_converter[cleantitles[i]] = years[i]
			try: 
				summary_converter[cleantitles[i]] += str(summaries[i])
			except: 
				summary_converter[cleantitles[i]] = str(summaries[i])
		if 'wiki' in file:
			wikititles = cleantitles
		elif 'imdb' in file:
			imdbtitles = cleantitles
		elif 'flixable' in file:
			flixabletitles = cleantitles
		elif 'RottenTomatoes' in file:
			rottentomatoestitles = cleantitles
		elif 'allmovie' in file:
			allmovietitles = cleantitles
		print(file)
		#except:
		#	continue
			
all_titles = list(set(imdbtitles + flixabletitles + rottentomatoestitles+allmovietitles+wikititles))
print("Total number of titles: "+str(len(all_titles)))

"""
inthree = 0
imdbflix = 0
imdbrot = 0
flixrot = 0
imdb = 0
flix = 0
rot  =0

five = 0
four = 0
three = 0
two = 0
one = 0
for title in all_titles:
	count = 0
	if title in imdbtitles:
		count += 1
	if title in flixabletitles:
		count += 1
	if title in rottentomatoestitles:
		count += 1 
	if title in allmovietitles:
		count += 1
	if title in wikititles or title.split('-')[0]+'-' in wikititles:
		count += 1
	if count == 5:
		five += 1
	elif count == 4:
		four += 1
	elif count == 3:
		three += 1
	elif count == 2:
		two += 1
	elif count == 1:
		one += 1
print("In five: "+str(five))
print("In four: "+str(four))
print("In three: "+str(three))
print("In two: "+str(two))
print("In one: "+str(one))
print(five+four+three+two+one)
"""

"""
for title in all_titles:
	#print(title)
	if title in imdbtitles and title in flixabletitles and title in rottentomatoestitles:
		inthree += 1
	elif title in imdbtitles and title in flixabletitles:
		imdbflix += 1
	elif title in imdbtitles and title in rottentomatoestitles:
		imdbrot += 1
	elif title in flixabletitles and title in rottentomatoestitles:
		flixrot += 1
	elif title in imdbtitles:
		imdb += 1
	elif title in flixabletitles:
		flix += 1
	elif title in rottentomatoestitles:
		rot += 1
print("In all three: "+str(inthree))
print("in IMDb and Flixable: "+str(imdbflix))
print("In IMDb and Rotten Tomatoes: "+str(imdbrot))
print("In Rotten Tomatoes and Flixable: "+str(flixrot))
print("Only in IMDb: "+str(imdb))
print("Only in Flixable: "+str(flix))
print("Only in RottenTomatoes: "+str(rot))
"""
#combined_df = pandas.DataFrame(columns=['title','cleantitle','year','combined_summaries'])
target_list = []
for cleantitle in all_titles:
	dict = {'title': title_converter[cleantitle],'cleantitle': cleantitle,'year': year_converter[cleantitle],'combined_summaries': summary_converter[cleantitle]}
	target_list.append(dict)

with open('combined_data.csv', 'w', encoding='utf-8',newline='') as f:
	writer = csv.DictWriter(f, fieldnames=['title','cleantitle','year','combined_summaries'])
	writer.writeheader()
	for data in target_list:
		writer.writerow(data)
