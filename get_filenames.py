from os import listdir
import urllib.parse

""""
path = "C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie"
base_url = 'https://www.allmovie.com/movie/' 
targetfile = 'AllMovie_urls.txt'

path = "C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\tmdb"
base_url = 'https://www.themoviedb.org/movie/' 
targetfile = 'TMDb_urls.txt'

path = "D:\\Downloads\\IMDb_pages"
base_url = 'https://www.imdb.com/title/' 
targetfile = 'IMDb_urls.txt'

path = "D:\\RTCrawler\\rottentomatoes"
base_url = 'https://www.rottentomatoes.com/m/' 
targetfile = 'RottenTomatoes_urls.txt'
"""
path = "D:\\wikicrawler\\wiki"
base_url = 'https://en.wikipedia.org/wiki/' 
targetfile = 'Wikipedia_urls.txt'

with open (targetfile, 'w+') as outfile:
	for name in listdir(path):
		url = base_url+urllib.parse.unquote(name.split('.')[0])
		outfile.write(url+'\n')
		
print("{} urls written to targetfile".format(len(listdir(path))))