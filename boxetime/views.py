from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import *
from django.contrib.auth import *
import re
from .forms import *
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView


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


class EventView(TemplateView):
    template_name = 'new_event.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context["form"] = NewCompetitionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = NewCompetitionForm(request.POST)
        if form.is_valid():
            formtemp = form.save(commit=False)
            formtemp.author = request.user
            formtemp.save()
            return redirect("/")


# class EventView(FormView):
#     template_name = 'new_event.html'
#     form_class = NewCompetitionForm
#     success_url = 'event/1'


def addrequest(request):
    form = AddRequestForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)
    event_number = form.cleaned_data['competit'].id
    return redirect(event, event_number)


def event_list(request):
    event_list = Competition.objects.all()
    return render(request, 'event_list.html', {"event_list": event_list})


@user_passes_test(lambda u: u.is_anonymous, login_url="/")
def signup(request):
    profileform = ProfileUpdateForm()
    userform = ExtendsUserCreationForm()
    if request.method == "POST":
        user_form = ExtendsUserCreationForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/')
    context = {'formprofile': profileform, 'formuser': userform}
    return render(request, 'signup.html', context=context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")
        else:
            messages.error(request, "Incorrect user data")
    form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    if 'next' in request.GET:
        return redirect(request.GET.get('next'))
    return redirect('/')


@login_required(login_url="/login")
def cabinet(request):
    if request.method == "POST":
        form = ExtnedsUserChangeForm(request.POST, instance=request.user)
        form_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and form_profile.is_valid():
            form.save()
            form_profile.save()
            return redirect("/profile/edit")
    user_form = ExtnedsUserChangeForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'cabinet.html', {'user_form': user_form, 'profile_form': profile_form})
