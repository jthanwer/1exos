from django.db.models import Avg
from filemanager.models import Exercice


def selfcorrec_points():
    value = Exercice.objects.all().aggregate(Avg('prix'))['prix__avg']
    return int(value)


def mean_prices():
    prices = {classe: 0 for classe in range(7)}
    for classe in range(7):
        qs = Exercice.objects.filter(niveau=classe)
        count = qs.count()
        if count > 0:
            value = qs.aggregate(Avg('prix'))['prix__avg']
            prices[classe] = int(value)
        else:
            prices[classe] = 0
    return prices


# -- Points données s'être enregistré
START_POINTS = 4

# -- 1€ = 4 points
CHANGE = 4

# -- 20% Bonus
BONUS = 0.2

# --------------
# -- Corrections
# --------------

MEAN_PRICES = mean_prices()

# -- Points données lorsque le correcteur corrige un exercice à lui
SELFCORREC_POINTS = selfcorrec_points()

# -- Points données lorsque le correcteur a dépassé la date limite
DEADLINE_POINTS = 3

# -- Points données lorsque ce n'est pas la première correction
MULTIPLECORREC_POINTS = 3
