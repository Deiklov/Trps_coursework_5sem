from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Competition(models.Model):
    sport_choices = (
        ('Boxing', 'Бокс'),
        ('Kickboxing', 'Кикбоксинг')
    )
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    place = models.CharField(max_length=255)
    responsible = models.TextField(blank=True)
    level = models.CharField(max_length=200)
    sport = models.CharField(max_length=50, choices=sport_choices, default='Boxing')
    description = models.TextField(blank=True)
    docs = models.FileField(upload_to='docs/', blank=True, null=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


class AddRequest(models.Model):
    role_choices = (
        ('Doctor', 'Врач'),
        ('Participant', 'Участник'),
        ('Coach', 'Тренер'),
        ('Sponsor', 'Cпонсор')
    )
    role = models.CharField(max_length=100, choices=role_choices, default='Participant')
    weight = models.PositiveSmallIntegerField()
    docs = models.FileField(upload_to='docs/', blank=True)
    competit = models.ForeignKey(Competition, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=2)
    acepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.userid) + " " + str(self.weight) + " " + self.role + " " + str(self.competit)


class CompetitGrid(models.Model):
    member1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='member1', null=True)
    member2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='member2', null=True)
    memberlist = (
        (member1, 'member1'),
        (member2, 'member2')
    )
    memberwin = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='memberwin', null=True)
    weight = models.PositiveSmallIntegerField(blank=True)
    levelgrid = models.PositiveSmallIntegerField(blank=True)
    competitid = models.ForeignKey(Competition, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.member1) + " vs " + str(self.member2) + " (" + str(self.weight) + ") " + str(self.competitid)
