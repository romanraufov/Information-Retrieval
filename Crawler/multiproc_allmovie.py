# multiproc_test.py
#https://stackoverflow.com/questions/2080660/python-multiprocessing-and-a-shared-counter

import multiprocessing
import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import os

target_folder = 'C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie'
base_url = 'https://www.allmovie.com/movie/'

#Global variables
access_lock = 0
num_procs = 10

def acquire_lock(access_lock):
	while True:
		if access_lock is 0:
			access_lock += 1
			return
		else:
			sleep(1)
			
def release_lock(access_lock):
	print(access_lock)
	if access_lock > 1:
		print("Something, somewhere went terribly wrong...")
	access_lock -= 1

def add_done(urls):
	with open('done.txt', 'a') as f:
		for url in urls:
			f.write(url+'\n')
	with open('done.txt', 'r') as f:
		return len(f.readlines())

def add_to_do(urls):
	to_do = get_to_do()
	done = get_done()
	with open('to_do.txt', 'a') as f:
		for url in urls:
			if url+'\n' not in to_do and url+'\n' not in done:
				f.write(url+'\n')

def get_done():
	with open('done.txt', 'r') as f:
		return f.readlines()
		
def get_to_do():
	with open('to_do.txt', 'r') as f:
		return f.readlines()
			
def pop_to_do(process_id, num_procs=num_procs):
	to_do = get_to_do()
	num_to_pop = (int)(len(to_do)/num_procs)
	if num_to_pop == 0 and len(to_do) > 0:
		num_to_pop = 1
	with open('to_do.txt', 'w') as f:
		if len(to_do) > 1: #if file is not empty after pop
			new_to_do = to_do[:len(to_do)-num_to_pop]
			if type(new_to_do) == list:
				for line in new_to_do:
					f.write(line)
			else:
				f.write(new_to_do)
			#if len(to_do[:len(to_do)-num_to_pop+1]) > 1:
			#	for line in to_do[:num_to_pop]:
			#		f.write(line)
		else:
			f.write('')
	return to_do[(len(to_do)-num_to_pop):]
		
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
	
def crawl(pages_to_collect, process_id, access_lock):
	urls = list()
	local_links = list()
	while True:
		#acquire_lock(access_lock)
		with access_lock.get_lock():
			print("access lock acquired by process "+process_id)
			if len(urls) > 0:
				done = add_done(urls)
				if done > pages_to_collect:
					return
			urls = [url.strip() for url in pop_to_do(str(process_id))]
			if len(local_links) > 1:
				add_to_do(local_links)
			local_links = list()
		#release_lock(access_lock)
		print("access lock released by process "+process_id)
		#try:
		for url in urls:
			page = get_page(url)
			store(page,url)
			movie_links = get_movie_links(page)
			local_links.extend(movie_links)
			print(url, 'succesfully stored by process ', str(process_id))
		#except:
		#	print('failed for url '+url+' by process '+str(process_id))		
		sleep(1)

if __name__ == "__main__":
	access_lock = multiprocessing.Value('i', 0)
	procs = num_procs   # Number of processes to create
	pages_to_collect = 1000
	# Create a list of jobs and then iterate through
	# the number of processes appending each process to
	# the job list
	jobs = []
	for i in range(0, procs):
		process = multiprocessing.Process(target=crawl,
			                              args=(pages_to_collect, str(i), access_lock))
		jobs.append(process)

	# Start the processes (i.e. calculate the random number lists)
	for j in jobs:
		j.start()

	# Ensure all of the processes have finished
	for j in jobs:
		j.join()
	
	print("Crawling complete.")