#'title', 'year','summary', "positive_sentiment","negative_sentiment", "imdb_url","tmdb_url","rottentomatoes_url","allmovie_url","rottentomatoes_tomatometer", "rottentomatoes_audiencescore", "allmovie_rating", "rottentomatoes_audiencerating", "imdb_rating", "allmovie_summary", "rottentomatoes_summary", "flixable_summary"



def buildMovieBlock(resultInfo):
    return False


def getSVG(PosSent, NegSent):
    total = int(PosSent) + int(NegSent)
    if total == 0:
        return ""
    perPos = int(int(PosSent) / total * 100)
    svg = """<svg viewBox="0 0 32 32"> <circle class='first' stroke-dasharray=" """+str(perPos)+""" 100 "></circle></svg>"""
    return svg

# def getBestSnippet(resultInfo):
#     listSums = ["summary", "rottentomatoes_summary", "allmovie_summary", "flixable_summary"]
#     bestSummary = "summary"
#     for summary in listSums:
#         if resultInfo[summary]:
#             bestSummary = summary
#             break
#     # return not more then 3 sentences
#     bestSnippet = resultInfo[bestSummary]
#     bestSnippet = bestSnippet.split(".")
#     if len(bestSnippet) < 4:
#         bestSnippet = ". ".join(bestSnippet)
#     else:
#         bestSnippet = ". ".join(bestSnippet[:3])
#     return bestSnippet

def getBestSnippet(resultInfo):
    listSums = ["rottentomatoes_summary", "allmovie_summary", "flixable_summary", "imdb_summary", "tmdb_summary", "wiki_summary"] # "summary" 
    maxLength = 30
    for summary in listSums:
        #print("resultInfo keys: ", resultInfo.keys())
        snippet = resultInfo[summary].split(" ")
        if len(snippet) > 3:
            if len(snippet) > maxLength:
                snippet = snippet[:maxLength - 1]
                break
    bestSnippet = " ".join(snippet)
    bestSnippet = bestSnippet + "..."
    return bestSnippet


def getSiteScores(resultInfo):
    nameSites = ["IMDb", "RottenTomatoes", "Allmovies"]
    listSites = ["imdb_url","rottentomatoes_url","allmovie_url"]
    listScores = ["imdb_rating", "rottentomatoes_audiencerating", "allmovie_rating"]
    scoresInHtml = ""
    for i in range(len(listScores)):
        if hasNumbers(resultInfo[listScores[i]]):
            print("QH- score present:", resultInfo[listScores[i]], " from site: ", listSites[i])
            scoresInHtml += """<span><a href= """+resultInfo[listSites[i]]+""">"""+nameSites[i]+"""</a>:"""+resultInfo[listScores[i]]+"""</span></br>"""
    if scoresInHtml:
        scoresInHtml = "<strong>Scores</strong></br>" + scoresInHtml
    return scoresInHtml

def hasNumbers(string2check):
    return any(char.isdigit() for char in string2check)
    

   