from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import *
from django.contrib.auth import *
from .forms import *
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.views.generic.edit import *
from django.views.generic.base import *
from django.views.generic.list import *
from django.views.generic.detail import *
import datetime


class Main(TemplateView):
    template_name = 'index.html'


# def update_grid(request, eventid):
#     formset = GridFormSet(request.POST, queryset=CompetitGrid.objects.filter(competitid=eventid).order_by('weight'))
#     for form in formset:
#         if form.is_valid():
#             form.save()
#     return redirect(event, eventid)


class SearchView(ListView):
    template_name = "search_template.html"
    context_object_name = "event_list"

    def get_queryset(self):
        search_query = self.request.GET.get('search_region', None)
        if search_query:
            return Competition.objects.filter(place__icontains=search_query)
        search_query = self.request.GET.get('search_title', None)
        if search_query:
            return Competition.objects.filter(title__icontains=search_query)
        search_query = self.request.GET.get('search_date', None)
        if search_query:
            date = datetime.datetime.strptime(search_query, "%Y-%m-%d")
            return Competition.objects.filter(date__lte=date)


class EventViewDetail(DetailView):
    template_name = 'event.html'
    model = Competition
    pk_url_kwarg = 'eventid'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventViewDetail, self).get_context_data(**kwargs)
        context['members'] = AddRequest.objects.select_related().filter(competit=kwargs.get(self.pk_url_kwarg),
                                                                        acepted=True)
        context['addrequests'] = AddRequest.objects.filter(competit=kwargs.get(self.pk_url_kwarg), acepted=False)
        context['addrequestform'] = AddRequestForm(kwargs.get(self.pk_url_kwarg), self.request.user)
        return context

    # def event(request, number):
    #     weight = int(request.GET.get('weight', default=75))
    #     event = Competition.objects.get(pk=number)
    #     # if (event.date < datetime.date.today()):
    #     #     make_pair(number)
    #     members = AddRequest.objects.select_related().filter(competit=number, acepted=True)
    #     compgrid = GridFormSet(initial=[{'competitid': number}],
    #                            queryset=CompetitGrid.objects.filter(competitid=number, weight__range=(
    #                                weight, weight_tuple[weight_tuple.index(weight) + 1])).order_by(
    #                                'weight'))
    #     addrequests = AddRequest.objects.filter(competit=number, acepted=False)
    #     addrequestform = AddRequestForm(number, request.user)
    #     context = {"event": event, "number": number,
    #                'addrequestform': addrequestform, 'addrequests': addrequests,
    #                'members': members, 'grid': compgrid, 'weight_tuple': weight_tuple}
    #     return render(request, 'event.html', context=context)


# def req_handler(request, req_id, flag):
#     addrequest = AddRequest.objects.get(pk=req_id)  # забрали реквест из бд
#     eventid = addrequest.competit.id
#     if flag == 1:  # добавляем запись в бд
#         user = User.objects.get(pk=addrequest.userid.id)
#         cometition = Competition.objects.get(pk=eventid)
#         cometition.users.add(user)
#         addrequest.acepted = True
#         cometition.save()
#         addrequest.save()
#     elif flag == 0:
#         addrequest.delete()
#     return redirect(event, eventid)


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


class AddRequestView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return str('/event/%d' % kwargs.get('eventid'))

    def get(self, request, *args, **kwargs):
        form = AddRequestForm(self.request.user, request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.competit = Competition.objects.get(pk=kwargs.get('eventid'))
            form.save()
        return super().get(request, *args, **kwargs)


# def addrequest(request, number):
#     # competit = Competition.objects.get(pk=number)
#     form = AddRequestForm(number, request.user, request.POST)
#     if form.is_valid():
#         ff = form.save(commit=False)
#         ff.competit = Competition.objects.get(pk=number)
#         ff.save()
#     return redirect(event, number)


class EventListView(ListView):
    template_name = "event_list.html"
    model = Competition
    context_object_name = "event_list"


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


class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        else:
            return "/"

    def form_valid(self, form):
        username = self.request.POST["username"]
        password = self.request.POST["password"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Incorrect user data")
        return super().form_invalid(form)


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return '/'

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super().get(request, *args, **kwargs)


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
