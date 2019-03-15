def get_results(query):
	html = ''
	results = [{'name':'The Avengers','url':'https://www.imdb.com/title/tt0848228/?ref_=nv_sr_3','url_platform':'IMDb','year':'2012'}]
	for result in results:
		result_html = embed_result(result)
		html += result_html
	return html
	
def embed_result(result):
	name = result['name']
	url = result['url']
	url_platform = result['url_platform']
	year = result['year'] 
	html = """<div class="row justify-content-md-center source-card">
							<div class="col-sm-12 col-md-11">
								<div class="card mb-3">
									<div class="card-body">
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
															URL <a href=\""""+url+"""\" target="_blank"><strong><u>"""+url_platform+"""</u></strong></a>
															<br>
															Jaar: <strong>"""+year+"""</strong>
														</div>
														<div class="col-md content">Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.<br>
														<br>
														</div>
													</div>
												</div>
											</div>
											<div class="col-sm-12 mt-2 mt-md-0 col-md-3 options justify-content-center d-flex  align-items-center">
											<strong>Scores</strong>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>"""
	return html