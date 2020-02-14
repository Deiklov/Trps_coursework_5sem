from django.test import TestCase, Client
from django.urls import reverse
from boxetime.models import *
import random


class TestViews(TestCase):
    def test_get_request(self):
        client = Client()
        response = client.get(reverse('event_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_list.html')


class TestEventList(TestCase):
    def setUp(self):
        user = User.objects.create_user('somename', 'myemail@crazymail.com', 'password')
        title = ('заголовок 1', "заголвоок 2", "заголовок 3", "заголовок 4", "заголовок 5")
        city = ('Москва', "Хабаровск", "Магадан", "Чкаловск", "Балахна")
        responsbile = ('Карим', "Ахмед", "Витя", "Петя", "Коля")
        level = ('Первенство ПФО', "Первенство Москвы", "Чемпионат России", "А", "Б")
        sport = ('Бокс', "Кикбоксинг")
        descript = ('описание 1', "описание 2", "описание 3", "описание 4", "описание 5")
        docs = ('')
        date = timezone.now().date()
        Competition.objects.create(title='Некторый заголовок', place="Город Х", responsible="Царь",
                                   level="Турнир класса Е", sport="Кикбоксинг", description="Некоторое описание",
                                   docs="",age=12,
                                   author_id=user.id, date=timezone.now().date())
        for x in range(1, 5000):
            Competition.objects.create(title=random.choice(title), place=random.choice(city),
                                       level=random.choice(level), sport=random.choice(sport),
                                       description=random.choice(descript), docs=docs,
                                       author_id=user.id, date=date, age=0,
                                       responsible=random.choice(responsbile))

    def test_load_page(self):
        client = Client()
        response = client.get(reverse('event_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_list.html')


