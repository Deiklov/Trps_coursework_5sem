from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Competition(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    place = models.CharField(max_length=255)
    responsible = models.TextField()
    level = models.CharField(max_length=200)
    sport = models.CharField(max_length=50)
    description = models.TextField()
    docs = models.FileField(upload_to='docs/', blank=True)

    def __str__(self):
        return self.title


class AddRequest(models.Model):
    role_choices = (
        ('Boxing', 'Бокс'),
        ('Kickboxing', 'Кикбоксинг')
    )
    year_in_school = models.CharField(max_length=50, choices=role_choices, default='Бокс')
    role = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField()
    docs = models.FileField(upload_to='docs/', blank=True)
    competit = models.ForeignKey(Competition, on_delete=models.CASCADE)
