from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from .models import *
from .forms import *


def main(request):
    return render(request, 'index.html', {})


def update_grid(request, eventid):
    GridFormSet = modelformset_factory(CompetitGrid, form=GridForm)
    formset = GridFormSet(request.POST, queryset=CompetitGrid.objects.filter(competitid=eventid).order_by('weight'))
    if formset.is_valid():
        formset.save()
    return redirect(event, eventid)


def event(request, number):
    event = Competition.objects.get(pk=number)
    members = AddRequest.objects.select_related().filter(competit=number, acepted=True)
    GridFormSet = modelformset_factory(CompetitGrid, form=GridForm)
    compgrid = GridFormSet(initial=[{'competitid': number}],
                           queryset=CompetitGrid.objects.filter(competitid=number).order_by('weight'))
    addrequests = AddRequest.objects.filter(competit=number, acepted=False)
    addrequestform = AddRequestForm(initial={'competit': number})
    context = {"event": event, "number": number,
               'addrequestform': addrequestform, 'addrequests': addrequests,
               'members': members, 'grid': compgrid}
    return render(request, 'event.html', context=context)


def req_handler(request, req_id, flag):
    addrequest = AddRequest.objects.get(pk=req_id)  # забрали реквест из бд
    eventid = addrequest.competit.id
    if flag == 1:  # добавляем запись в бд
        user = User.objects.get(pk=addrequest.userid.id)
        cometition = Competition.objects.get(pk=eventid)
        cometition.users.add(user)
        addrequest.acepted = True
        cometition.save()
        addrequest.save()
    elif flag == 0:
        addrequest.delete()
    return redirect(event, eventid)


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
