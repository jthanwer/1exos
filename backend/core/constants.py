from filemanager.models import Exercice
from django.db.models import Avg, Max
from django.db.models import Count
from django.db import connection
from datetime import datetime, timezone

now = datetime.now(timezone.utc)

# -- Points données après s'être enregistré
def START_POINTS():
    return 20


# -- 1€ = 4 points
def CHANGE():
    return 4


# -- 20% Bonus
def BONUS():
    return 0.2

# --------------
# -- Corrections
# --------------

def START_CORREC_PRICE():
    return 1


def MEAN_PRICES():
    prices = {niveau: 0 for niveau in range(7)}
    for niveau in range(7):
        qs = Exercice.objects.annotate(num_c=Count('correcs'))
        qs = qs.filter(niveau=niveau)
        count = qs.count()
        if count > 0:
            value = qs.aggregate(Avg('prix'))['prix__avg']
            prices[niveau] = round(value)
        else:
            prices[niveau] = -1
    return prices


def MAX_PRICES():
    prices = {niveau: 0 for niveau in range(7)}
    for niveau in range(7):
        qs = Exercice.objects.annotate(num_c=Count('correcs'))
        qs = qs.filter(niveau=niveau, num_c=0, date_limite__gt=now)
        count = qs.count()
        if count > 0:
            value = qs.aggregate(Max('prix'))['prix__max']
            prices[niveau] = round(value)
        else:
            prices[niveau] = -1
    return prices


# -- Points données lorsque le correcteur corrige un exercice à lui
def SELFCORREC_POINTS():
    return 1
    # qs = Exercice.objects.all()
    # if qs.count() > 0:
    #     value = Exercice.objects.all().aggregate(Avg('prix'))['prix__avg']
    # else:
    #     value = -1
    # return int(value)


# -- Points données lorsque le correcteur a dépassé la date limite
def DEADLINE_POINTS():
    return 1

# -- Points données lorsque ce n'est pas la première correction
def MULTIPLECORREC_POINTS():
    return 1
