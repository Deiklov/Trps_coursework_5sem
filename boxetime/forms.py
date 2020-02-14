from django import forms
from .models import *
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class NewCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = "__all__"
        labels = {"title": "Название", 'date': 'Дата', 'place': 'Место проведения', 'responsible': 'Ответственные',
                  'age': "Минимальный возраст участников", "level": "Уровень соревнований", "sport": "Вид спорта",
                  "description": "Описание", "docs": "Организационные документы"}
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}),
                   'author': forms.HiddenInput(),
                   'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
                   'responsible': forms.Textarea(attrs={'rows': 3, 'cols': 15})}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(pk=user.id)
        self.fields['author'].initial = User.objects.get(pk=user.id)

    def clean(self):
        super(NewCompetitionForm, self).clean()
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Слишком короткий заголовок')
        author = self.cleaned_data.get('author')
        if not User.objects.get(pk=author.id):
            raise forms.ValidationError('Проблемы с автором')
        data = self.cleaned_data.get('date')
        if not data > timezone.now().date():
            raise forms.ValidationError('Дата создания должна быть больше сегодняшнего дня')
        return self.cleaned_data


class AddRequestForm(forms.ModelForm):
    class Meta:
        model = AddRequest
        exclude = ('userid', 'acepted', 'competit')
        labels = {"weight": "Вес", "docs": "Персональный документы", "role": "Ваша роль", "rank": 'Разряд',
                  'club': "Спортивный клуб"}

    def clean(self):
        super(AddRequestForm, self).clean()
        role = self.cleaned_data.get('role')
        if role != 'Participant':
            self.cleaned_data['weight'] = None
            self.cleaned_data['rank'] = None
        else:
            if self.cleaned_data.get('rank') == None or self.cleaned_data.get('weight') == None:
                raise forms.ValidationError("Обязательное поле")
        return self.cleaned_data


class GridForm(forms.ModelForm):
    member1 = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, label='Красный',
                                     widget=forms.Select(attrs={'readonly': 'readonly'}))
    member2 = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, label='Синий',
                                     widget=forms.Select(attrs={'readonly': 'readonly'}))
    memberwin = forms.ModelChoiceField(queryset=User.objects.all(), label='Побед', empty_label=None)

    class Meta:
        model = CompetitGrid
        fields = "__all__"
        labels = {
            "levelgrid": "Уровень",
            "weight": "Вес"
        }
        widgets = {'competitid': forms.HiddenInput(),
                   'levelgrid': forms.TextInput(attrs={'readonly': 'readonly', 'size': '2'}),
                   'weight': forms.TextInput(attrs={'readonly': 'readonly', 'size': '2'})}

    def clean(self):
        super(GridForm, self).clean()
        member1 = self.cleaned_data.get('member1')
        member2 = self.cleaned_data.get('member2')
        memberwin = self.cleaned_data.get('memberwin')
        if memberwin != member1 and memberwin != member2:
            raise forms.ValidationError("Победитель должен быть одним из участников")
        return self.cleaned_data

    def __init__(self, *args, eventid, weight, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(eventid, int):
            alluserfromevent = AddRequest.objects.filter(competit_id=eventid, weight=weight).values(
                'userid_id').distinct()
            self.base_fields['member1'].queryset = User.objects.filter(id__in=alluserfromevent)
            self.base_fields['member2'].queryset = User.objects.filter(id__in=alluserfromevent)
            self.base_fields['memberwin'].queryset = User.objects.filter(id__in=alluserfromevent)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Логин")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': "form-control"}),
                               label="Пароль")


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class ExtendsUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    username = forms.CharField(max_length=60, label="Логин")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # labels = {'email': 'Электронная почта',"username":"логин"}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class ExtnedsUserChangeForm(forms.ModelForm):
    email = forms.EmailField(label="Электронная почта")

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {'avatar': "Персональная картинка"}


GridFormSet = modelformset_factory(model=CompetitGrid, form=GridForm, extra=0)
