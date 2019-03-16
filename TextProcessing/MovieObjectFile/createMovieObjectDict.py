import csv
import pickle

csv2convert = "C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\MovieObjectFile\\combineddata_cleaned.csv"

movieObjectDict = {}

with open(csv2convert, "r", encoding="utf8") as csvMovie:
    reader = csv.reader(csvMovie)
    counter = 0 
    for row in reader:
        counter += 1
        if counter > 0:
            # "tmbd_summary":row[4], "flixable_summary":row[5], "rottentomatoes_summary":row[6], "allmovie_summary":row[7], "wiki_summary":row[8], "imdb_synopsis":row[9], imdb_url:row[10], "tmdb_url":row[11], "rottentomatoes_url":row[12], "allmovie_url":row[13], "imdb_sentiment":row[14], "imdb_rating":row[15], "tmdb_rating":row[16], "rottentomatoes_tomatometer":row[17],  "rottentomatoes_audiencescore":row[18],  "rottentomatoes_audiencerating":row[19],  "rottentomatoes_criticsrating":row[20],  "allmovie_rating":row[21],  "all_summaries":row[22],  "tmdb_rating":row[23], 
            movieObjectDict[row[1]] = {'title': row[0], 'year': row[2], 'summary':row[3], "positive_sentiment":row[23], "negative_sentiment":row[24], "imdb_url":row[10], "tmdb_url":row[11], "rottentomatoes_url":row[12], "allmovie_url":row[13], "rottentomatoes_tomatometer":row[17], "rottentomatoes_audiencescore":row[18], "allmovie_rating":row[21], "rottentomatoes_audiencerating":row[19], "imdb_rating":row[15], "allmovie_summary":row[7], "rottentomatoes_summary":row[6], "flixable_summary":row[5]}
    csvMovie.close()



len(movieObjectDict.keys())



pickle_out = open("C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\MovieObjectFile\\MovieObjects.pickle","wb")
pickle.dump(movieObjectDict, pickle_out)
pickle_out.close()