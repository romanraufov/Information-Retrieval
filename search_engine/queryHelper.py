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

def getBestSnippet(resultInfo):
    listSums = ["summary", "rottentomatoes_summary", "allmovie_summary", "flixable_summary"]
    bestSummary = "summary"
    for summary in listSums:
        if resultInfo[summary]:
            bestSummary = summary
            break
    # return not more then 3 sentences
    bestSnippet = resultInfo[bestSummary]
    bestSnippet = bestSnippet.split(".")
    if len(bestSnippet) < 4:
        bestSnippet = ". ".join(bestSnippet)
    else:
        bestSnippet = ". ".join(bestSnippet[:3])
    return bestSnippet


