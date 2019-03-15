from django.shortcuts import render
from django.http import HttpResponse
import os
from querier import get_results
# Create your views here.

def index(request):
	return render(request, "search_engine.html", {})

def query(request):
	enteredQuery = str(request.body, 'utf-8')
	# retrieve document from results
	moviePointers = getMoviePointers(enteredQuery)
	

	# return movieObject by parsing the found documents in the MovieObject CSV
	movieObjects = getMovieObjects(moviePointers)

	# put list of movieObjects in get_results


	print("query in views: ", enteredQuery)
	html = get_results(request)
	return HttpResponse(html)


def getMoviePointers(enteredQuery):

	return False

def getMovieObjects(listOfMoviePointers):

	return False