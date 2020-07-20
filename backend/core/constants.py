from django.db.models import Avg
from filemanager.models import Exercice
from django.db import connection

# -- Points données s'être enregistré
def START_POINTS():
    return 4


# -- 1€ = 4 points
def CHANGE():
    return 4


# -- 20% Bonus
def BONUS():
    return 0.2

# --------------
# -- Corrections
# --------------


def MEAN_PRICES():
    prices = {classe: 0 for classe in range(7)}
    for classe in range(7):
        qs = Exercice.objects.filter(niveau=classe)
        count = qs.count()
        if count > 0:
            value = qs.aggregate(Avg('prix'))['prix__avg']
            prices[classe] = int(value)
        else:
            prices[classe] = -1
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
    return 3
