from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
import re
from django.http import Http404


def main(request):
    return render(request, 'index.html', {})


def event(request, number):
    return render(request, 'event.html')


def new_event(request):
    return render(request, 'new_event.html', )


def login(request):
    return render(request, 'login.html', )


def signup(request):
    return render(request, 'signup.html', )
