from django.test import SimpleTestCase
from django.urls import reverse, resolve
from boxetime.views import *


class TestUrls(SimpleTestCase):
    def test_base_url(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)
