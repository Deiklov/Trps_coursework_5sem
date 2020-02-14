from django.test import SimpleTestCase, Client
from django.urls import reverse, resolve
from boxetime.views import *


class TestUrls(SimpleTestCase):
    def test_base_url(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_new_event_url(self):
        response = self.client.get(reverse('new_event'))
        self.assertGreaterEqual(response.status_code, 200)
        self.assertLessEqual(response.status_code, 302)

    def test_new_event_incorrect_url(self):
        response = self.client.get('event400')
        self.assertEquals(response.status_code, 404)

    def test_new_event_incorrect_url(self):
        response = self.client.get(reverse('personal_results'))
        self.assertGreaterEqual(response.status_code, 200)
        self.assertLessEqual(response.status_code, 302)
