

#reset all crawlers
import os
path = os.getcwd() + "\\"
    
fullPath_allmovie = path + "allmovie_to_do.txt"
open(fullPath_allmovie, 'w+').close()
open(path + "allmovie_done.txt", "w+").close()
allMovie = open(fullPath_allmovie, 'w', encoding='utf-8')
allMovie.write("https://www.allmovie.com/" + "\n")
allMovie.close()

fullPath_flixable = path + "flixable_to_do.txt"
open(fullPath_flixable, 'w+').close()
open(path + "flixable_done.txt", "w+").close()
allMovie = open(fullPath_flixable, 'w', encoding='utf-8')
allMovie.write("https://flixable.com/title/80201449" + "\n")
allMovie.close()

fullPath_imdb = path + "imdb_to_do.txt"
open(fullPath_imdb, 'w+').close()
open(path + "imdb_done.txt", "w+").close()
allMovie = open(fullPath_imdb, 'w', encoding='utf-8')
allMovie.write("https://www.imdb.com/title/tt5316540" + "\n")
allMovie.close()

fullPath_rottentomatoes = path + "rottentomatoes_to_do.txt"
open(fullPath_rottentomatoes, 'w+').close()
open(path + "rottentomatoes_done.txt", "w+").close()
allMovie = open(fullPath_rottentomatoes, 'w', encoding='utf-8')
allMovie.write("https://www.rottentomatoes.com/top/" + "\n")
allMovie.close()


