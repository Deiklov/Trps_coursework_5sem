from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Competition(models.Model):
    sport_choices = (
        ('Boxing', 'Бокс'),
        ('Kickboxing', 'Кикбоксинг')
    )
    title = models.CharField(max_length=100)
    date = models.DateField()
    place = models.CharField(max_length=255)
    responsible = models.TextField(blank=True)
    age = models.PositiveSmallIntegerField(blank=True)
    level = models.CharField(max_length=200)
    sport = models.CharField(max_length=50, choices=sport_choices, default='Boxing')
    description = models.TextField(blank=True)
    docs = models.FileField(upload_to='docs/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/event/%s" % (self.id)


class AddRequestManager(models.Manager):
    def save(self, objects_list, user, **kwargs):
        if not AddRequest.objects.filter(userid=user, competit_id=kwargs.get('eventid')).exists():
            self.create(role=objects_list['role'],
                        weight=objects_list['weight'],
                        competit_id=kwargs.get('eventid'),
                        userid=user,
                        docs=objects_list['docs'],
                        rank=objects_list['rank'])


class AddRequest(models.Model):
    role_choices = (
        ('Doctor', 'Врач'),
        ('Participant', 'Участник'),
        ('Coach', 'Тренер'),
        ('Sponsor', 'Cпонсор'),
        ('Referee', 'Судья'),
    )
    ranks = (
        ('novice', 'Новичок'),
        ('third', 'Третий разряд'),
        ('second', 'Второй разряд'),
        ('first', 'Первый разряд'),
        ('kms', 'КМС'),
        ('master', 'Мастер спорта'),
    )
    weight_choice = (
        (60, '[0,60)'), (64, '[60;64)'), (69, '[64,69)'), (75, '[69,75)'), (81, '[75,81)'), (91, '[81,91)'),
        (500, '[91+)'),
    )
    role = models.CharField(max_length=100, choices=role_choices, default='Participant')
    weight = models.PositiveSmallIntegerField(choices=weight_choice, default=75, blank=True, null=True)
    docs = models.FileField(upload_to='docs/', blank=True)
    competit = models.ForeignKey(Competition, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.SET(1), default=1)
    acepted = models.BooleanField(default=False)
    rank = models.CharField(max_length=50, choices=ranks, default='novice', blank=True, null=True)
    club = models.CharField(max_length=255, blank=True, null=True)
    objects = AddRequestManager()

    def __str__(self):
        return str(self.userid) + " " + "max " + str(self.weight) + ")" + " " + self.role + " " + str(self.competit)


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


class Profile(models.Model):
    avatar = models.ImageField(default="default.png", upload_to="images/")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


weight_tuple = (60, 64, 69, 75, 81, 91, 500)
