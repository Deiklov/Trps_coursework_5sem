from django.test import TestCase
from boxetime.forms import *
import datetime


class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('TestUser', 'lennon@thebeatles.com', 'john')

    def test_new_event_form(self):
        # user = User.objects.create_user('TestUser', 'lennon@thebeatles.com', 'john')
        form = NewCompetitionForm(self.user, data={
            'title': 'Новое соревнование',
            'place': 'Москва',
            'responsible': 'Василий Олегович Ромашкин',
            'level': 'Городские',
            'sport': 'Boxing',
            'description': 'Городские соревнования, первые в 2020 году',
            'author': self.user.id,
            'age': 25,
            'date': datetime.date(2025, 6, 7)
        })
        status = form.is_valid()
        self.assertTrue(status)

    def test_AddRequestForm(self):
        form = AddRequestForm(data={
            'role': 'Participant',
            'weight': 91,
            'userid': self.user.id,
            'sport': 'Boxing',
            'acepted': False,
            'rank': 'kms',
            'club': "MGTU"
        })
        status = form.is_valid()
        self.assertTrue(status)

    def test_NewCompetitionForm(self):
        # user = User.objects.create_user('TestUser', 'lennon@thebeatles.com', 'john')
        form = NewCompetitionForm(self.user, data={
            'title': 'Новое соревнование',
            'place': 'Москва',
            'responsible': 'Василий Олегович Ромашкин',
            'level': 'Городские',
            'sport': 'Boxing',
            'description': 'Городские соревнования, первые в 2020 году',
            'author': self.user.id,
            'age': 25,
            'date': datetime.date(2018, 6, 7)
        })
        status = form.is_valid()
        self.assertFalse(status)
