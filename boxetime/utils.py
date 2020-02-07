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
    if CompetitGrid.objects.filter(competitid_id=eventid):  # есть ли сетка
        check_all_level(eventid)  # проверяем иф шо секонд сплит
    else:
        while i < len(weight_tuple) - 1:  # for first split
            people = participant.filter(weight__range=[weight_tuple[i], weight_tuple[i + 1] - 1]).order_by(
                "-rank")  # список участников в этом весе
            n = people.count()
            if n == 0:
                i += 1
                continue
            # kk = math.floor(math.log(2, 2))
            j = math.floor(math.log(n, 2))  # floor степень для участников, example 50->2^5, j=5
            jbig = math.ceil(math.log(n, 2))
            free_people = 2 ** jbig - n
            pair_count = math.trunc((n - free_people) / 2)
            if n == 1:
                free_people = 1
                pair_count = 0
                n += 1
            j = 0
            while j < pair_count * 2:
                member1 = people[j].userid
                member2 = people[j + 1].userid
                weight = weight_tuple[i]
                competitid = eventid
                levelgrid = math.ceil(math.log(n, 2))  # логарифм числа участников
                CompetitGrid.objects.create(member1=member1, member2=member2, memberwin=None, weight=weight,
                                            competitid_id=competitid, levelgrid=levelgrid)
                j += 2  # перескочили через противника
            while j < free_people + pair_count * 2:  # сделали экстра пары(онли при первом этапе)
                member1 = people[j].userid
                member2 = people[j].userid
                memberwin = people[j].userid  # сам же выиграл
                weight = weight_tuple[i]
                competitid = eventid
                levelgrid = math.ceil(math.log(n, 2))  # логарифм числа участников
                CompetitGrid.objects.create(member1=member1, member2=member2, memberwin=memberwin, weight=weight,
                                            competitid_id=competitid, levelgrid=levelgrid)
                j += 1
            i += 1


def check_level(compid, levelid, weight):  # проверит один конкретный уровень
    participant = CompetitGrid.objects.filter(competitid=compid, levelgrid=levelid, weight=weight)
    if not participant:
        return False
    for member in participant:
        if not member.memberwin:  # чекаем, заполнены ли победители
            break
    else:
        return True  # вернет True если прошел весь цикл
    return False  # false если по брейку выбежал


def check_all_level(compid):
    i = 0  # just testing must be i=0
    while i < len(weight_tuple):
        minlevel = CompetitGrid.objects.filter(competitid=compid, weight=weight_tuple[i]).order_by('-levelgrid').values(
            'levelgrid')
        if minlevel.first():
            minlevel = minlevel.first()['levelgrid']  # вытащили минимальный уровень(int)
        else:
            i += 1
            continue  # нет пар в весе
        particip = CompetitGrid.objects.filter(competitid=compid, weight=weight_tuple[i],
                                               levelgrid__exact=minlevel)  # участники с minlevel
        n = particip.count()
        level = math.ceil(math.log(n * 2, 2))  # глубочайших левел
        while level >= 1:
            if not check_level(compid, level, weight_tuple[i]):  # не заполнен
                level -= 1
                break
            else:
                if not CompetitGrid.objects.filter(competitid=compid, levelgrid=level - 1, weight=weight_tuple[
                    i]):  #есть ли объекты с пред левелом
                    # if not check_level(compid, level - 1, weight_tuple[i]):
                    secondary_splitting(compid, level, weight_tuple[i])  # сплит только 1 раз
                level -= 1
        i += 1


# учитываем вес тк на разные веса разное кол-во уровней
def secondary_splitting(compid, levelid, weight):
    if levelid == 1:
        return False
    participant = CompetitGrid.objects.filter(competitid=compid, levelgrid=levelid, weight=weight)
    j = 0
    while j < participant.count():
        member1 = participant[j].memberwin
        member2 = participant[j + 1].memberwin
        competitid = compid
        levelgrid = levelid - 1  # стпень показывающая
        CompetitGrid.objects.create(member1=member1, member2=member2, weight=weight,
                                    competitid_id=competitid, levelgrid=levelgrid)
        j += 2
    return True
