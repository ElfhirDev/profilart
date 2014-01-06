from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from work.models import *

def home(request):
    searchObject = request.POST
    searchWord = searchObject.get('the_search')
    return render(request, 'searchengine/home.html', locals())

def computeTableIndex(request):
    works = Work.objects.all()
    for work in works:
        words = work.name.split()
        for word in words:
            print word
    
    return render(request, 'searchengine/computeTableIndex.html', locals())
    
    #text = """<h1>Table Index Computed</h1>"""
    #return HttpResponse(text)
