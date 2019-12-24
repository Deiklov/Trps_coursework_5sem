from .models import *
from .forms import *
import math

ranks = (
    ('novice', 'Новичок'),
    ('third', 'Третий разряд'),
    ('second', 'Второй разряд'),
    ('first', 'Первый разряд'),
    ('kms', 'КМС'),
    ('master', 'Мастер спорта'),
)


# делает начальную разбивку всех весов ставя каждому свой уровень
def make_pair(eventid):
    participant = AddRequest.objects.filter(competit=eventid, acepted=True)
    i = 0
    # check all level in weight if true when secondary_splitting
    while i < len(weight_tuple):  # for first split
        people = participant.filter(weight__range=[weight_tuple[i], weight_tuple[i + 1]]).order_by(
            "-rank")  # список участников в этом весе
        n = people.count()
        j = math.floor(math.log(n, 2))
        count_pair_binary = 2 ** (j - 1)  # те кто уложился в степень двойки
        extra_people = 2 ** (j + 1) - n  # те кто проходят изи в следующий тур
        extra_pair = (n - extra_people - count_pair_binary * 2) / 2  # те кто выше двойки но дерутся за след тур
        j = 0
        while j < count_pair_binary + extra_pair:
            compgrid = CompetitGrid()
            compgrid.member1 = people[j]
            compgrid.member2 = people[j + 1]
            compgrid.weight = weight_tuple[i]
            compgrid.competitid = eventid
            compgrid.levelgrid = int(math.sqrt(count_pair_binary) * 2)  # стпень показывающая
            compgrid.save()
            j += 2
        j = 0
        while j < extra_people:
            compgrid = CompetitGrid()
            compgrid.member1 = people[j]
            compgrid.member2 = people[j]
            compgrid.memberwin = people[j]  # сам же выиграл
            compgrid.weight = weight_tuple[i]
            compgrid.competitid = eventid
            compgrid.levelgrid = int(math.sqrt(count_pair_binary) * 2)  # стпень показывающая
            compgrid.save()
            j += 1


def check_level(compid, levelid, weight):
    participant = CompetitGrid.objects.filter(competitid=compid,
                                              levelgrid=levelid,
                                              weight=weight)  # можно игнорить вес, запустим только если все провели бои
    for member in participant:
        if not member.memberwin:
            break
    else:
        return True  # вернет True если прошел весь цикл
    return False  # false если по брейку выбежал


def check_all_level(compid):
    i = 0
    while i < len(weight_tuple):
        particip =


# учитываем вес тк на разные веса разное кол-во уровней
def secondary_splitting(compid, levelid, weight):
    if levelid == 1:
        return False
    participant = CompetitGrid.objects.filter(competitid=compid, levelgrid=levelid, weight=weight).order_by("-rank")
    j = 0
    while j < participant.count():
        compgrid = CompetitGrid()
        compgrid.member1 = participant[j]
        compgrid.member2 = participant[j + 1]
        compgrid.weight = weight
        compgrid.competitid = compid
        compgrid.levelgrid = levelid - 1  # стпень показывающая
        compgrid.save()
        j += 2
    return True
