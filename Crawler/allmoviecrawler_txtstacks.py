import requests
from bs4 import BeautifulSoup
from time import sleep
import re

"""
Notes on politeness:
- Only /movie/ pages are requested, which is allowed by the robots.txt
- Between each request there is one second delay to limit the crawling frequency
- Only relevant pages (/movie/) are requested, limiting the number of total requests
"""

target_folder = 'C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie'
base_url = 'https://www.allmovie.com/movie/'

#done = [] #Array of movie page url's that have already been visited
#to_do = ['https://www.allmovie.com/movie/incredibles-2-v596222'] #Array of movie page url's that have yet to be visited. Initialized with one url

def add_done(url):
	with open('done.txt', 'a') as f:
		f.write(url+'\n')

def add_to_do(url):
	with open('to_do.txt', 'r') as f:
		to_do = f.readlines()
	if url+'\n' not in to_do:
		with open('to_do.txt', 'a') as f:
			f.write(url+'\n')

def get_done():
	with open('done.txt', 'r') as f:
		return f.readlines()
		
def pop_to_do():		
	with open('to_do.txt') as f:
		to_do = f.readlines()
	with open('to_do.txt', 'w') as f:
		if len(to_do[:-1]) > 0:
			for line in to_do[:-1]:
				f.write(line+'\n')
		else:
			f.write('')
	return to_do[-1]
		
#Given a url, return the content of the page as string
def get_page(url):
	response = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
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
	
while True:
	url = pop_to_do().strip()
	try:
		page = get_page(url)
		store(page,url)
		movie_links = get_movie_links(page)
		for link in movie_links:
			if link+'\n' not in get_done():
				add_to_do(link)
		add_done(url)
		print(url, 'succesfully stored')
	except:
		print('failed for url '+url)		
	sleep(1)