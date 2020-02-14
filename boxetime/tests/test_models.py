from django.test import TestCase
from boxetime.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
        Competition.objects.create(title='Некторый заголовок', place="Город Х", responsible="Царь",
                                   level="Турнир класса Е", sport="Кикбоксинг", description="Некоторое описание",
                                   docs="", age=23,
                                   author_id=self.user.id, date=datetime.date(2025, 6, 7))

    def test_new_competition(self):
        event = Competition.objects.get(title='Некторый заголовок')
        self.assertEqual(event.sport, 'Кикбоксинг')

    def test_authenticate(self):
        auth_user = authenticate(username='myusername', password='mypassword')
        self.assertTrue(auth_user is not None and auth_user.is_authenticated)

    def test_wrong_password(self):
        auth_user = authenticate(username='myusername', password='mypad')
        self.assertFalse(auth_user is not None and auth_user.is_authenticated)

    def tearDown(self):
        self.user.delete()


class CompetitionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
        Competition.objects.create(title='Некторый заголовок', place="Город Х", responsible="Царь",
                                   level="Турнир класса Е", sport="Кикбоксинг", description="Некоторое описание",
                                   docs="", age=23,
                                   author_id=self.user.id, date=datetime.date(2025, 6, 7))

    def test_new_competition(self):
        event = Competition.objects.get(title='Некторый заголовок')
        self.assertEqual(event.sport, 'Кикбоксинг')

    def test_addrequest(self):
        event = Competition.objects.get(title='Некторый заголовок')
        addrequest = AddRequest.objects.create(role='Participant', weight=81, docs="", acepted=True, rank='kms',
                                               competit_id=event.id, userid_id=self.user.id, club="Клуб")
        self.assertEqual(addrequest.role, 'Participant')
        self.assertEqual(addrequest.rank, 'kms')
        self.assertNotEqual(addrequest.club, 'Клааб')

    def tearDown(self):
        self.user.delete()
