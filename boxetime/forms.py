from django import forms
from .models import NewCompetition


class NewCompetitionForm(forms.ModelForm):
    class Meta:
        model = NewCompetition
        fields = "__all__"
        labels = {"title": "Название"}
