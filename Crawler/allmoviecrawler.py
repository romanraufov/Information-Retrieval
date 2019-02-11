import requests
from bs4 import BeautifulSoup
from time import sleep
import re


target_folder = 'C:\\xampp\\htdocs\\IR_DS2019\\Crawler'
base_url = 'https://www.allmovie.com/movie/'

done = [] #Array of movie page url's that have already been visited
to_do = ['https://www.allmovie.com/movie/incredibles-2-v596222'] #Array of movie page url's that have yet to be visited. Initialized with one url

import urllib

#Given a url, return the content of the page as string
def get_page(url):
	response = requests.get(url, headers ={"user-agent":"Mozilla/5.0"})
	return response.text
	
def store(page, url):
	code = url.split('/movie/')[1]
	file_name = target_folder+'\\'+code+'.txt'
	file = open(file_name, 'w+', encoding='utf-8')
	file.write(page)
	file.close()

#Given a the content of a page in string format, return the links to other movies it contains
def get_movie_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [a['href'] for a in soup.findAll('a', href=True)]
	movielinks = [base_url+re.split('\?|\/',link)[2] for link in links if link.startswith('/movie')]
	return movielinks
	
while len(to_do) > 0:
	url = to_do.pop()
	try:
		page = get_page(url)
		store(page,url)
		movie_links = get_movie_links(page)
		for link in movie_links:
			if link not in done and link not in to_do:
				to_do.append(link)
		done.append(url)
		print(url, 'succesfully stored')
	except:
		print('failed for url '+url)		
	sleep(1)