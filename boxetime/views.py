from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *


def main(request):
    return render(request, 'index.html', {})


def event(request, number):
    return render(request, 'event.html')


def new_event(request):
    form = NewCompetitionForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'new_event.html', {"form": form})


def event_list(request):
    event_list = NewCompetition.objects.all()
    return render(request, 'event_list.html', {"event_list": event_list})


# def login(request):
#     return render(request, 'registration/login.html', )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
