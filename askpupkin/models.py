from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Profile(models.Model):
    avatar = models.ImageField(blank=True, null=True, upload_to="images/")
    reg_data = models.DateField()
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    tag_word = models.CharField(max_length=80)

    def __str__(self):
        return self.tag_word


class QuestionManager(models.Manager):
    def best_questions(self):
        return self.order_by('-rating')

    def newest_questions(self):
        return self.order_by('-data_create')


class Question(models.Model):
    title = models.CharField(max_length=255)
    data_create = models.DateField(default=datetime.date.today())
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    @property
    def answer_count(self):
        return self.answer_set.count()


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    data_create = models.DateField()
    rating = models.IntegerField(default=0)
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.author) + " " + str(self.content)
