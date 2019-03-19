from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
from querier import get_results
import ast
# Create your views here.

sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\QueryProcessing\\')
import mainQueryProcessing as QP
import MovieObjectRetriever as MOR

def index(request):
	return render(request, "search_engine.html", {})

def query(request):
	#fullquery = ast.literal_eval(str(request.body, 'utf-8'))
	# send request.body contains [currentQuery, currentTitle, currentKeyWords, [formerQuery, formerTitle, formerKeywords], eachResult[rank, pointer, evalvalue]]
	print("request.body in views: ", request.body)
	fullquery = ast.literal_eval(str(request.body, 'utf-8'))
	print("request: ", fullquery)
	# fullquery = [0:query, 1:TitleCheckbox, 2:KeywordsCheckbox]
	enteredQuery = fullquery[0]

	# retrieve document from results
	
	#print(moviePointers)
	checkboxTitle = fullquery[1]
	checkboxSummary = fullquery[2]
	# when checkbox input can be retrieved
	if checkboxTitle == "True" and checkboxSummary == "True":
		print("first checkbox statement")
		moviePointers = getMoviePointers(enteredQuery)
	elif checkboxTitle == "True" and checkboxSummary != "True":
		print("second checkbox statement")
		moviePointers = getMoviePointersTitleQuery(enteredQuery)
	else: 
		print("last checkbox statement")
		moviePointers = getMoviePointersSummaryQuery(enteredQuery)
	# return movieObject by parsing the found documents in the MovieObject CSV
	movieObjects = getMovieObjects(moviePointers)

	# put list of movieObjects in get_results
	print("query in views: ", enteredQuery)
	html = get_results(movieObjects)
	return HttpResponse(html)

def getMoviePointers(enteredQuery):
	topMoviePointers = QP.mainProcessor(enteredQuery)
	return topMoviePointers

def getMoviePointersTitleQuery(enteredQuery):
	topMoviePointers = QP.ProcessTitleQuery(enteredQuery)
	return topMoviePointers

def getMoviePointersSummaryQuery(enteredQuery):
	topMoviePointers = QP.ProcessQuery(enteredQuery)
	return topMoviePointers

def getMovieObjects(listOfMoviePointers):
	MovieInfoRanked = MOR.getMovieInfo(listOfMoviePointers)
	return MovieInfoRanked