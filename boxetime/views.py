from django.shortcuts import render, redirect, HttpResponseRedirect
from .utils import *
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib.auth.decorators import *
from django.contrib.auth import *
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import *
from django.views.generic.base import *
from django.views.generic.list import *
from django.views.generic.detail import *
import datetime


class Main(TemplateView):
    template_name = 'index.html'


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
        search_query = self.request.GET.get('search_age', None)
        if search_query:
            return Competition.objects.filter(age__lte=search_query)


class EventViewDetail(DetailView):  # основная страница соревнования
    template_name = 'event.html'
    model = Competition
    pk_url_kwarg = 'eventid'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventViewDetail, self).get_context_data(**kwargs)
        weight = self.request.GET.get('weight', 75)
        context['weight'] = weight
        eventid = kwargs.get('object').id
        if Competition.objects.get(pk=eventid).date < timezone.now().date():
            make_pair(eventid)
        context['members'] = AddRequest.objects.select_related().filter(competit=context['object'].id,
                                                                        acepted=True)
        if not self.request.user.is_anonymous:
            context['is_written'] = AddRequest.objects.filter(competit_id=eventid, userid_id=self.request.user)
            if AddRequest.objects.filter(userid_id=self.request.user.id, competit_id=eventid, acepted=True,
                                         role='Doctor'):
                context['is_doctor'] = True
            else:
                context['is_doctor'] = False
        context['author'] = Competition.objects.get(pk=eventid).author.username
        context['grid'] = GridFormSet(form_kwargs={'eventid': eventid, 'weight': weight},
                                      queryset=CompetitGrid.objects.filter(competitid=eventid, weight=weight).order_by(
                                          "levelgrid"))
        context['weight_tuple'] = weight_tuple
        context['addrequests'] = AddRequest.objects.filter(competit=context['object'].id, acepted=False)
        context['addrequestform'] = AddRequestForm()
        return context


class ChangeGrid(RedirectView):
    def get(self, request, *args, **kwargs):
        forms = GridFormSet(request.POST, form_kwargs={'eventid': kwargs['eventid'], 'weight': kwargs['weight']})
        for form in forms:
            if form.is_valid():
                form.save()
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return str('/event/%d?weight=%d' % (kwargs.get('eventid'), kwargs['weight']))


# новый евент

class EventView(TemplateView):
    template_name = 'new_event.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context["form"] = NewCompetitionForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = NewCompetitionForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            return self.render_to_response({'form': form})


# добавить заявку
class AddRequestView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return str('/event/%d' % kwargs.get('eventid'))

    def get(self, request, *args, **kwargs):
        form = AddRequestForm(request.POST, request.FILES)
        if form.is_valid():
            AddRequest.objects.save(form.cleaned_data, request.user, **kwargs)
        return super().get(request, *args, **kwargs)


# accept or reject request
class AddMemberHandler(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return str('/event/%d' % kwargs['event_id'])

    def get(self, request, *args, **kwargs):
        acept = kwargs['flag']
        req_id = kwargs['req_id']
        addrequest = AddRequest.objects.get(pk=req_id)
        doctor = AddRequest.objects.filter(userid_id=self.request.user.id, competit_id=kwargs['event_id'], acepted=True,
                                           role='Doctor')
        admin_id = Competition.objects.get(pk=addrequest.competit_id).author_id
        if doctor or self.request.user.id == admin_id:
            if acept == 1:
                addrequest.acepted = True
                addrequest.save()
            elif acept == 0:
                addrequest.delete()
        return super().get(request, *args, **kwargs)


# удалить соревнование
class DeleteEventHandler(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('event_list')

    def get(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        admin_id = Competition.objects.get(pk=event_id).author_id
        if self.request.user.id == admin_id:
            competit = get_object_or_404(Competition, pk=event_id)
            competit.delete()
        return super().get(request, *args, **kwargs)


# список всех евентов
class EventListView(ListView):
    template_name = "event_list.html"
    model = Competition
    context_object_name = "event_list"


class PersonalResultsView(View):
    def get(self, *args, **kwargs):
        firstDate = self.request.GET.get('search_date_from', None)
        secondDate = self.request.GET.get('search_date_to', None)
        if firstDate and secondDate:
            dateFrom = datetime.datetime.strptime(firstDate, "%Y-%m-%d")
            dateTo = datetime.datetime.strptime(secondDate, "%Y-%m-%d")
            listCompetit = AddRequest.objects.filter(userid=self.request.user.id, acepted=True).values_list(
                'competit_id').distinct()
            levelArray = []
            for x in listCompetit:
                maxlevel = CompetitGrid.objects.filter(competitid_id__in=x, memberwin=self.request.user.id).order_by(
                    'levelgrid').values_list('levelgrid').first()
                if maxlevel:
                    levelArray.append(int(maxlevel[0]) + 1)
                else:
                    levelArray.append(int(maxlevel[0]))
            placeArray = list(map(lambda x: str(2 ** (x - 1) + 1) + '--' + str(2 ** x), levelArray))
            listCompetit = Competition.objects.filter(date__lte=dateTo, date__gte=dateFrom, id__in=listCompetit)
            return render(self.request, 'personal_results.html', {'competit': listCompetit, 'place': placeArray})
        return render(self.request, 'personal_results.html')


# ниже регистрация login logout update_form
@method_decorator(user_passes_test(lambda u: u.is_anonymous, login_url="/"), name='dispatch')
class SingUpView(View):
    def get(self, *args, **kwargs):
        profileform = ProfileUpdateForm()
        userform = ExtendsUserCreationForm()
        context = {'formprofile': profileform, 'formuser': userform}
        return render(self.request, 'signup.html', context=context)

    def post(self, *args, **kwargs):
        user_form = ExtendsUserCreationForm(self.request.POST)
        profile_form = ProfileUpdateForm(self.request.POST, self.request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(self.request, username=username, password=password)
            login(self.request, user)
            return redirect('/')
        else:
            context = {'formprofile': profile_form, 'formuser': user_form}
            return render(self.request, 'signup.html', context=context)


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
        messages.error(self.request, "Неверные данные, поищите ошибку в логине или пароле")
        return super().form_invalid(form)


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return '/'

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super().get(request, *args, **kwargs)


class CabinetView(View):
    def post(self, *args, **kwargs):
        form = ExtnedsUserChangeForm(self.request.POST, instance=self.request.user)
        form_profile = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        if form.is_valid() and form_profile.is_valid():
            form.save()
            form_profile.save()
            return redirect("/profile/edit")

    def get(self, *args, **kwargs):
        user_form = ExtnedsUserChangeForm(instance=self.request.user)
        profile_form = ProfileUpdateForm(instance=self.request.user.profile)
        return render(self.request, 'cabinet.html', {'user_form': user_form, 'profile_form': profile_form})
