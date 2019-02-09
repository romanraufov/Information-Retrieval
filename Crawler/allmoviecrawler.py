import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import urllib.parse
import urllib.request
import requests

"""
Notes on politeness:
- Only /movie/ pages are requested, which is allowed by the robots.txt
- Between each request there is one second delay to limit the crawling frequency
- Only relevant pages (/movie/) are requested, limiting the number of total requests

Requests failed:
<p>The following error was encountered while trying to retrieve the URL: <a href="http://www.allmovie.com/movie/incredibles-2-v596222">http://www.allmovie.com/movie/incredibles-2-v596222</a></p>

<blockquote id="error">
<p><b>Access Denied.</b></p>
</blockquote>

<p>Access control configuration prevents your request from being allowed at this time. Please contact your service provider if you feel this is incorrect.</p>

<p>Your cache administrator is <a href="mailto:webmaster?subject=CacheErrorInfo%20-%20ERR_ACCESS_DENIED&amp;body=CacheHost%3A%20gce-all-proxy04%0D%0AErrPage%3A%20ERR_ACCESS_DENIED%0D%0AErr%3A%20%5Bnone%5D%0D%0ATimeStamp%3A%20Thu,%2007%20Feb%202019%2011%3A14%3A15%20GMT%0D%0A%0D%0AClientIP%3A%20130.211.1.77%0D%0A%0D%0AHTTP%20Request%3A%0D%0AGET%20%2Fmovie%2Fincredibles-2-v596222%20HTTP%2F1.1%0AUser-Agent%3A%20python-requests%2F2.18.4%0D%0AAccept-Encoding%3A%20gzip,%20deflate%0D%0AAccept%3A%20*%2F*%0D%0AX-Cloud-Trace-Context%3A%2001a472807921b224a1ad06fbe7cc2c83%2F8445807696855045012%0D%0AVia%3A%201.1%20google%0D%0AX-Forwarded-For%3A%2087.195.7.188,%2035.186.213.14%0D%0AX-Forwarded-Proto%3A%20https%0D%0AConnection%3A%20Keep-Alive%0D%0AHost%3A%20www.allmovie.com%0D%0A%0D%0A%0D%0A">webmaster</a>.</p>
"""

target_folder = 'C:/Users/chris/OneDrive/Documenten/DataScience/InformationRetrieval/ScrapedSites/AllMovie'
base_url = 'https://www.allmovie.com/movie/'

done = [] #Array of movie page url's that have already been visited
to_do = ['https://www.allmovie.com/movie/incredibles-2-v596222'] #Array of movie page url's that have yet to be visited. Initialized with one url

# necessary for allmovie, otherwise they don't let us in
headers = {
    'User-Agent': 'Robot from the UvA, http://www.uva.nl/',
    'From': '10645012@student.uva.nl'
}


#Given a url, return the content of the page as string
def get_page(url):
	response = requests.get(url, headers = headers)
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

def mainAllMovie(maxRounds = -1):
	"""
	Executes Allmovie crawler. Enter value for maximum number of pages to be scraped
	saves the textfiles at a given file location
	"""
	counter = 0 
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
		if counter == maxRounds:
			print('Early stop crawler, {} pages have been crawled'.format(counter))
			break
		else:
			counter += 1
	if maxRounds == -1:
		print("No more URL in crawling list anymore. The have been {} pages crawled. Congratz!".format(counter))
		

#run main
mainAllMovie(10)
