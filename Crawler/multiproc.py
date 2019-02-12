# multiproc_test.py

import multiprocessing
import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import os

target_folder = 'C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie'
base_url = 'https://www.allmovie.com/movie/'

to_do = ['https://www.allmovie.com/movie/the-lego-movie-2-the-second-part-v598909']
done = []
		
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
	
def crawl(pages_to_collect, process_id):
	while True:
		url = to_do.pop()
		#try:
		page = get_page(url)
		store(page,url)
		movie_links = get_movie_links(page)
		for link in movie_links:
			if link not in done and link not in to_do:
				to_do.append(link)
		done.append(url)
		print(url, 'succesfully stored by ', process_id)
		#except:
		#	print('failed for url '+url+' by '+process_id)		
		sleep(1)

if __name__ == "__main__":
	procs = 2   # Number of processes to create
	pages_to_collect = 2
	# Create a list of jobs and then iterate through
	# the number of processes appending each process to
	# the job list
	jobs = []
	for i in range(0, procs):
		process = multiprocessing.Process(target=crawl,
			                              args=(pages_to_collect, str(i)))
		jobs.append(process)

	# Start the processes (i.e. calculate the random number lists)
	for j in jobs:
		j.start()

	# Ensure all of the processes have finished
	for j in jobs:
		j.join()
	
	print("Crawling complete.")