from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
import re
from django.http import Http404


def question_list(request, tag=None):
    path = request.path
    if path == '/hot':
        question_list = Question.objects.best_questions()
    elif re.match(r'^/tag/.+$', path):  # tag select
        question_list = Question.objects.filter(tag__tag_word=tag)
    else:
        question_list = Question.objects.newest_questions()
    page = paginate(question_list, request)
    paginator = page.paginator
    tags = Tag.objects.all()
    context = {'questions': page.object_list, 'tags': tags,
               'page': page, 'paginator': paginator}
    return render(request, 'index.html', context=context)


def competition(request, number):
    answers = Answer.objects.filter(question=number)
    question = Question.objects.filter(id=number)
    return render(request, 'competition.html', {'answers': answers, 'questions': question})


def new_competition(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'new_competition.html', context=context)


def login(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'login.html', context=context)


def signup(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'signup.html', context=context)


def paginate(object_list, request):
    try:
        limit = int(request.GET.get('limit', 5))
    except ValueError:
        limit = 5
    if limit > 100:
        limit = 5
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(object_list, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
