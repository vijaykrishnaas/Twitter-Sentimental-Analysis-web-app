from django.shortcuts import render
from django.http import HttpResponse
import json

# import Main Module
from .module.main import getDateList, processSearchQuery, export


def index(request):
    context = dict()
    context["dates"] = getDateList()
    return render(request, 'sentiment/index.html', context)


def searchQuery(request):
    result = processSearchQuery(request)
    return render(request, 'sentiment/results.html', result)


def export(request):
    if request.method == 'POST':
        return export(request.body)
