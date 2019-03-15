from django.shortcuts import render
from django.http import HttpResponse
import os
from querier import get_results
# Create your views here.

def index(request):
	return render(request, "search_engine.html", {})

def query(request):
	html = get_results(request)
	return HttpResponse(html)
