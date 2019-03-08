import os
import requests
import datetime
from time import sleep

base_dir = os.getcwd()
folders = ['imdb']#,'tmdb','allmovie','rottentomatoes','flixable','wikipedia']

today = datetime.date.today()

#Given a url, return the content of the page as string
def get_page(url):
	response = requests.get(url, headers=headers)
	return response.text

#Extract code that is used for filename from the url
def get_code(url):
	code = ''
	if 'allmovie' in url:
		code = url.split('/movie/')[1]
	elif 'imdb' in url or 'flixable' in url:
		code = url.split('/title/')[1].split('/')[0]
	elif 'rottentomatoes' in url:
		code = url.split('/m/')[1].split('/')[0]
	elif 'tmdb' in url:
		code = url.split('/movie/')[1]
	elif 'wikipedia' in url:
		code = url.split('/wiki/')[1]
	return code

def store(target_folder, page, url):
	code = get_code(url)
	file_name = target_folder+'\\'+code+'.txt'
	with open(file_name, 'w+', encoding='utf-8') as file:
		file.write(page)
		
for folder in folders:
	folderbase_dir = base_dir+'\\'+folder
	logfile_name = folderbase_dir+'\\logfile.txt'
	
	#Read logfile
	with open(logfile_name, 'r') as logfile:
		entries = logfile.readlines()
		
	#Loop over files	
	for i in range(len(entries)):
		entry = entries[i]
		elements = entry.split('\t')
		if len(elements) > 1: #filter out empty lines
			url = elements[0]
			date = elements[1]
			date_parts = [int(part) for part in date.split('-')]
			scrape_date = datetime.date(date_parts[0],date_parts[1],date_parts[2])
			diff = today - scrape_date
			if diff.days > 30:
				#Update stored file, rename old version with extension _old
				filename = folderbase_dir+'\\'+get_code(url)
				os.rename(filename+'.txt',filename+'_old.txt')
				page = get_page(url)
				#page = "Hoi"
				store(folderbase_dir, page, url)
				entries[i] = url+'\t'+str(today)
				sleep(1)
			
	#Update logfile
	with open(logfile_name, 'w') as logfile:
		for entry in entries:
			logfile.write(entry+'\n')
			
