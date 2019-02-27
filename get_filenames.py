from os import listdir

path = "C:\\Users\\flori\\OneDrive\\Documenten\\Information Retrieval\\allmovie"
base_url = 'https://www.allmovie.com/movie/' 
targetfile = 'AllMovie_urls.txt'

with open (targetfile, 'w+') as outfile:
	for name in listdir(path):
		url = base_url+name.split('.')[0]
		outfile.write(url+'\n')
		
print("{} urls written to targetfile".format(len(listdir(path))))