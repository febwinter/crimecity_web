from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def mainView(request):
    return render(request, 'mapNnews/mapNews.html')