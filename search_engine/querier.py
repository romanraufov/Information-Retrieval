import sys

sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\search_engine')
import queryHelper as QH

def get_results(query):
	html = ''
	#results = [{'name':'The Avengers','url':'https://www.imdb.com/title/tt0848228/?ref_=nv_sr_3','url_platform':'IMDb','year':'2012'}]
	results = query
	resultCounter = 0
	for result in results:
		result_html = embed_result(result, str(resultCounter))
		html += result_html
		resultCounter += 1
	return html
	
def embed_result(result, number):
	name = result['title']
	cleanTitle = result['cleantitle']
	year = result['year'].split(".")[0]
	posSentiment = result["positive_sentiment"]
	negSentiment = result["negative_sentiment"]
	
	# url = result['url']
	# url_platform = result['url_platform']
	#year = result['year'] 
	html = """<div class="row justify-content-md-center source-card">
							<div class="col-sm-12 col-md-8">
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
"""+QH.getSiteScores(result)+"""
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="slider-box col-sm-12 col-md-3">
								<div class="slider-wrapper">
									<span class="slider-label">0</span>
									<input id="SliderResult-"""+number+"""-"""+cleanTitle+"""" class="evaluationSlider" type="range" min="0" max="4" step="1"/>
									<span class="slider-label">4</span>
								</div>
							</div>
						</div>"""
	return html



# <span><a href= """+urlIMDB+"""> IMDb</a>:"""+scoreIMDB+"""</span></br>
# 											<span><a href= """+urlRotTom+""">RottenTomatoes</a>:"""+scoreRomTom+"""</span></br>
# 											<span><a href= """+urlAllmovie+""">Allmovies</a>:"""+scoreAllMovie+"""</span>