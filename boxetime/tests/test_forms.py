from django.test import SimpleTestCase
from boxetime.forms import *


class TestForms(SimpleTestCase):
    def test_new_event_form(self):
        form = NewCompetitionForm(data={
            'title': 'Новое соревнование',
            'place': 'Москва',
            'responsible': 'Василий Олегович Ромашкин',
            'level': 'Городские',
            'sport': 'Boxing',
            'description': 'Городские соревнования, первые в 2020 году',
        })
        self.assertTrue(form.is_valid())

    def test_new_event_form_false(self):
        form = NewCompetitionForm(data={
            'title': 'Новое соревнование',
            'responsible': 'Василий Олегович Ромашкин',
            'level': 'Городские',
            'sport': 'Boxing',
            'description': 'Городские соревнования, первые в 2020 году',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
