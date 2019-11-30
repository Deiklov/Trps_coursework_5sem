from django.test import TestCase, Client
from django.urls import reverse
from boxetime.models import *
import json


class TestViews(TestCase):
    def test_get_request(self):
        client = Client()
        response = client.get(reverse('event_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_list.html')
