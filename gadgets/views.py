from django.http import HttpResponse
from django.shortcuts import render


def index(reqest):
    return HttpResponse('hello world')
