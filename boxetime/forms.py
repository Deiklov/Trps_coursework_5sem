from django import forms
from .models import *
from django.forms import modelformset_factory

class NewCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = "__all__"
        labels = {"title": "Название"}


class AddRequestForm(forms.ModelForm):
    class Meta:
        model = AddRequest
        fields = "__all__"
        labels = {"weight": "Вес", "docs": "Персональный документы", "role": "Ваша роль"}
        widgets = {'competit': forms.HiddenInput()}


class GridForm(forms.ModelForm):
    member1 = forms.ModelChoiceField(queryset=User.objects.all())
    member2 = forms.ModelChoiceField(queryset=User.objects.all())
    memberwin = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = CompetitGrid
        fields = "__all__"
        widgets = {'competitid': forms.HiddenInput()}


GridFormSet = modelformset_factory(CompetitGrid, form=GridForm)
