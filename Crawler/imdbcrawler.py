import requests
from bs4 import BeautifulSoup
from time import sleep
import re

"""
Notes on politeness:
- Only /title/ pages are requested, which is allowed by the robots.txt
- Between each request there is one second delay to limit the crawling frequency
- Only relevant pages (/title/) are requested, limiting the number of total requests
"""

target_folder = 'D:\Downloads\Movie_pages'
base_url = 'https://www.imdb.com/title/'

done = [] #Array of movie page url's that have already been visited
to_do = ['https://www.imdb.com/title/tt0133093'] #Array of movie page url's that have yet to be visited. Initialized with one url

#Given a url, return the content of the page as string
def get_page(url):
	response = requests.get(url)
	return response.text
	
def store(page, url):
	code = url.split('/title/')[1].split('/')[0]
	file_name = target_folder+'\\'+code+'.txt'
	file = open(file_name, 'w+', encoding='utf-8')
	file.write(page)
	file.close()

#Given a the content of a page in string format, return the links to other movies it contains
def get_movie_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [a['href'] for a in soup.findAll('a', href=True)]
	movielinks = [base_url+re.split('\?|\/',link)[2] for link in links if link.startswith('/title')]
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