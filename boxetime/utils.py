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
    participant = AddRequest.objects.filter(competit=eventid, acepted=True)  # выбрали всех участников
    i = 0
    # check all level in weight if true when secondary_splitting
    while i < len(weight_tuple):  # for first split
        people = participant.filter(weight__range=[weight_tuple[i], weight_tuple[i + 1] - 1]).order_by(
            "-rank")  # список участников в этом весе
        n = people.count()
        if n == 0:
            i += 1
            continue
        j = math.floor(math.log(n, 2))  # floor степень для участников, example 50->2^5, j=5
        jbig = math.ceil(math.log(n, 2))
        pair_count = n - j
        free_people = jbig - n
        j = 0
        while j < pair_count * 2:
            member1 = people[j].userid
            member2 = people[j + 1].userid
            weight = weight_tuple[i]
            competitid = eventid
            levelgrid = math.ceil(math.sqrt(math.log(n, 2)))  # логарифм числа участников
            CompetitGrid.objects.create(member1=member1, member2=member2, memberwin=None, weight=weight,
                                        competitid_id=competitid, levelgrid=levelgrid)
            j += 2  # перескочили через противника
        j = 0
        while j < free_people:  # сделали экстра пары(онли при первом этапе)
            member1 = people[j].userid
            member2 = people[j].userid
            memberwin = people[j].userid  # сам же выиграл
            weight = weight_tuple[i]
            competitid = eventid
            levelgrid = math.ceil(math.sqrt(math.log(n, 2)))  # логарифм числа участников
            CompetitGrid.objects.create(member1=member1, member2=member2, memberwin=memberwin, weight=weight,
                                        competitid_id=competitid, levelgrid=levelgrid)
            j += 1
        i += 1


def check_level(compid, levelid, weight):
    participant = CompetitGrid.objects.filter(competitid=compid, levelgrid=levelid, weight=weight)
    for member in participant:
        if not member.memberwin:  # чекаем, заполнены ли победители
            break
    else:
        return True  # вернет True если прошел весь цикл
    return False  # false если по брейку выбежал


def check_all_level(compid):
    i = 0
    while i < len(weight_tuple):
        particip = CompetitGrid.objects.filter(competitid=compid, weight=weight_tuple[i])
        level = math.ceil(math.sqrt(math.log(particip, 2)))  # глубочайших левел
        while level >= 1:
            if check_level(compid, level, weight_tuple[i]):
                level -= 1
            else:
                secondary_splitting(compid, level, weight_tuple[i])


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
