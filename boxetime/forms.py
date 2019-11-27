from django import forms
from .models import *


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
