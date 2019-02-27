import wikipediaapi
import urllib

#This version print to stdout, so write to txt file with > name_of_txt_file in commmandline
#This is no scraper, it uses an API
"""
target_folder = 'D:\\Downloads\\Wikimoviepages\\'

def store(text, file_name):
	file = open(target_folder+file_name, 'w+', encoding='utf-8')
	file.write(text)
	file.close()
"""

wiki_wiki = wikipediaapi.Wikipedia('en')
cat = wiki_wiki.page("Category:Star Wars films")
#print("Category members: Category:English-language films")
for p in cat.categorymembers.values():
	text = ''
	if p.namespace == wikipediaapi.Namespace.MAIN: #if it is an article page
		try:
			#print(p.title)
			text += '\n'
			text += ' Hier begint een titel! '
			text += p.title
			text += ' Hier eindigt een titel! '
			text += '\n'
			text += p.text
			print(text)
			#title = urllib.parse.quote(p.title)
			#title = title.replace('/','slash')
			#file_name = title+'.txt'
			#store(p.txt, file_name)
		except:
			print('')
		
#store(text, 'allwikifiles.txt')