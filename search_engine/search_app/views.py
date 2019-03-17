from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
from querier import get_results
# Create your views here.

sys.path.insert(0, 'C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\QueryProcessing\\')
import mainQueryProcessing as QP
import MovieObjectRetriever as MOR

def index(request):
	return render(request, "search_engine.html", {})

def query(request):
	enteredQuery = str(request.body, 'utf-8')
	print("request: ", request)

	# retrieve document from results
	
	#print(moviePointers)
	checkboxTitle = True
	checkboxSummary = True
	# when checkbox input can be retrieved
	if checkboxTitle and checkboxSummary:
		moviePointers = getMoviePointers(enteredQuery)
	elif checkboxTitle and not checkboxSummary:
		moviePointers = getMoviePointersTitleQuery(enteredQuery)
	else: 
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