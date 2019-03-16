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
	# retrieve document from results
	moviePointers = getMoviePointers(enteredQuery)
	print(moviePointers)

	# return movieObject by parsing the found documents in the MovieObject CSV
	movieObjects = getMovieObjects(moviePointers)

	# put list of movieObjects in get_results
	print("query in views: ", enteredQuery)
	html = get_results(movieObjects)
	return HttpResponse(html)

def getMoviePointers(enteredQuery):
	topMoviePointers = QP.topRank(enteredQuery)
	return topMoviePointers

def getMovieObjects(listOfMoviePointers):
	MovieInfoRanked = MOR.getMovieInfo(listOfMoviePointers)
	return MovieInfoRanked