#https://stackoverflow.com/questions/2080660/python-multiprocessing-and-a-shared-counter

import multiprocessing
import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import os
import sys

#Global variables
target_folder = os.getcwd()+'\\allmovie'
base_url = 'https://www.allmovie.com/'

to_do_file = 'allmovie_to_do.txt'
done_file = 'allmovie_done.txt'

headers = {
    'User-Agent': 'Robot from the UvA, http://www.uva.nl/',
    'From': '10645012@student.uva.nl'
}

#Append urls to the done file
def add_done(urls):
	with open(done_file, 'a') as f:
		for url in urls:
			f.write(url+'\n')

#Append urls to the to_do file if they are not yet in either the to_do or the done file
def add_to_do(urls):
	urls = list(set(urls))
	to_do = get_to_do()
	done = get_done()
	with open(to_do_file, 'a') as f:
		for url in urls:
			if url+'\n' not in to_do and url+'\n' not in done:
				f.write(url+'\n')

#Get the content of the done file as a list
def get_done():
	with open(done_file, 'r') as f:
		return f.readlines()

#Get the content of the to_do file as a list		
def get_to_do():
	with open(to_do_file, 'r') as f:
		return f.readlines()

#Remove a batch of urls from the to_do file and return them to the crawler for scraping			
def pop_to_do(process_id, num_procs):
	to_do = get_to_do()
	num_to_pop = (int)(len(to_do)/num_procs) # Number of urls to pop from the to_do stack
	if num_to_pop == 0 and len(to_do) > 0:
		num_to_pop = 1
	with open(to_do_file, 'w') as f:
		if len(to_do) > 1: #if file is not empty after pop
			new_to_do = to_do[:len(to_do)-num_to_pop] # Content of the to_do stack after popping
			if type(new_to_do) == list:
				for line in new_to_do:
					f.write(line)
			else: # Then it is probably just one line, in string format
				f.write(new_to_do) 
		else:
			f.write('')
	return to_do[(len(to_do)-num_to_pop):]
		
#Given a url, return the content of the page as string
def get_page(url):
	response = requests.get(url, headers=headers)
	return response.text
	
def store(page, url):
	code = url.split('/movie/')[1]
	file_name = target_folder+'\\'+code+'.txt'
	with open(file_name, 'w+', encoding='utf-8') as file:
		file.write(page)

#Given a the content of a page in string format, return the links to other movies it contains
def get_movie_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [a['href'] for a in soup.findAll('a', href=True)]
	movielinks = [base_url+re.split('\?|\/',link)[2] for link in links if link.startswith('/movie')]
	movielinks.extend([base_url + link[1:] for link in links if link.startswith('/genre')])
	return movielinks

# checks pages that are important for retrieving links, but must not be saved themselves
def checkURL(RotTomURL):
	reviewURL = "www.allmovie.com/movie"
	return True if reviewURL in RotTomURL else False
	
def crawl(pages_to_collect, process_id, access_lock, num_procs):
	urls = list() # Pages to crawl
	local_links = list() # Links retrieved by the crawler. Will be pushed to the shared to_do stack
	while True:
	
		#Communication phase with the shared stacks
		with access_lock.get_lock():
			print("access lock acquired by process "+process_id)
			if len(urls) > 0:
				add_done(urls)
				done = get_done()
				if len(done) > pages_to_collect:
					return
			urls = [url.strip() for url in pop_to_do(str(process_id), num_procs)] # Retrieve new urls to crawl from the to_do stack
			if len(local_links) > 1:
				add_to_do(local_links)
			local_links = list()
		print("access lock released by process "+process_id)
		
		#Crawling phase
		
		for url in urls:
			page = get_page(url)
			if checkURL(url):
				store(page,url)
			movie_links = get_movie_links(page)
			local_links.extend(movie_links)
			print(url, 'succesfully stored by process ', str(process_id))
		# except:
		# 	print('failed for url '+url+' by process '+str(process_id))		
		sleep(1*num_procs)

	
def main(args):
	access_lock = multiprocessing.Value('i', 0)
	pages_to_collect = int(args[0])
	num_procs = int(args[1])   # Number of processes to create
	# Create a list of jobs and then iterate through
	# the number of processes appending each process to
	# the job list
	jobs = []
	for i in range(0, num_procs):
		process = multiprocessing.Process(target=crawl,
			                              args=(pages_to_collect, str(i), access_lock, num_procs))
		jobs.append(process)

	# Start the processes (i.e. calculate the random number lists)
	for j in jobs:
		j.start()

	# Ensure all of the processes have finished
	for j in jobs:
		j.join()
	
	print("Crawling complete.")
	
if __name__ == "__main__":
	main(sys.argv[1:])