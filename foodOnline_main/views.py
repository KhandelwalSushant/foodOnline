from django.shortcuts import render
from django.http import HttpResponse

def home(response):
    return HttpResponse('hello world')