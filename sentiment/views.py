from django.shortcuts import render
from django.http import HttpResponse
import json
import asyncio

# import Main Module
from .module.main import getDateList, processSearchQuery, export, saveSearchQuery, getLogFormat


import logging
logger = logging.getLogger('sentiment')


def index(request):
    context = dict()
    context["dates"] = getDateList()
    logger.info(getLogFormat(request))
    return render(request, 'sentiment/index.html', context)


def searchQuery(request):
    result = asyncio.run(processSearchQuery(request))
    saveSearchQuery(request)
    logger.info(getLogFormat(request))
    return render(request, 'sentiment/results.html', result)


def export(request):
    if request.method == 'POST':
        return export(request.body)
