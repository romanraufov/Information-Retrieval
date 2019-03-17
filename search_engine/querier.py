import sys

sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\search_engine')
import queryHelper as QH

def get_results(query):
	html = ''
	#results = [{'name':'The Avengers','url':'https://www.imdb.com/title/tt0848228/?ref_=nv_sr_3','url_platform':'IMDb','year':'2012'}]
	results = query
	for result in results:
		result_html = embed_result(result)
		html += result_html
	return html
	
def embed_result(result):
	name = result['title']
	urlIMDB = str(result["imdb_url"])
	urlRotTom = str(result["rottentomatoes_url"])
	urlAllmovie = str(result["allmovie_url"])
	url_platform = "testPlatform" 
	year = result['year'].split(".")[0]
	summary = result['summary']
	posSentiment = result["positive_sentiment"]
	negSentiment = result["negative_sentiment"]
	scoreAllMovie = result["allmovie_rating"]
	scoreIMDB = result["imdb_rating"]
	scoreRomTom = result["rottentomatoes_audiencerating"]
	
	# url = result['url']
	# url_platform = result['url_platform']
	#year = result['year'] 
	html = """<div class="row justify-content-md-center source-card">
							<div class="col-sm-12 col-md-11">
								<div class="card mb-3">
									<div id="card-element" class="card-body">
										<div class="row">
											<div class="col-md">
												<div class="container">
													<div class="row">
														<div class="col-md title">
															<p>
																<strong>"""+name+"""</strong>
															</p>
														</div>
													</div>
												</div>
												<div class="container">
													<div class="row">
														<div class="col-md-3 info">
															Year: <strong>"""+year+"""</strong>
"""+QH.getSVG(posSentiment, negSentiment)+"""
														</div>
														<div class="col-md content">"""+QH.getBestSnippet(result)+"""<br>
														<br>
														</div>
													</div>
												</div>
											</div>
											<div class="col-sm-12 mt-2 mt-md-0 col-md-3 options justify-content-center align-items-center">
											<strong>Scores</strong></br>
											<span><a href= """+ urlIMDB + """> IMDb</a>:"""+scoreIMDB+"""</span></br>
											<span><a href= """+ urlRotTom + """>RottenTomatoes</a>:"""+scoreRomTom+"""</span></br>
											<span><a href= """+ urlAllmovie + """>Allmovies</a>:"""+scoreAllMovie+"""</span>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>"""
	return html


