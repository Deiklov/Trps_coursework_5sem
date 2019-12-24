from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class NewCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        exclude = ('author', 'users')
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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': "form-control"}))


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class ExtendsUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class ExtnedsUserChangeForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
