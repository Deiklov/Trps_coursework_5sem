from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *


def main(request):
    return render(request, 'index.html', {})


def event(request, number):
    event = Competition.objects.get(pk=number)
    addrequests = AddRequest.objects.filter(competit=number)
    addrequestform = AddRequestForm(initial={'competit': number})
    context = {"event": event, "number": number, 'addrequestform': addrequestform, 'addrequests': addrequests}
    return render(request, 'event.html', context=context)


def req_handler(request, req_id, flag):
    addrequest = AddRequest(pk=req_id)
    if flag == 1:  # добавляем запись в бд
    # связать юзера и соревнования и удалить реквест
    elif flag == 0:
    # удалить реквест
    return redirect(event, 1)


def new_event(request):
    form = NewCompetitionForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'new_event.html', {"form": form})


def addrequest(request):
    form = AddRequestForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)
    event_number = form.cleaned_data['competit'].id
    return redirect(event, event_number)


def event_list(request):
    event_list = Competition.objects.all()
    return render(request, 'event_list.html', {"event_list": event_list})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
