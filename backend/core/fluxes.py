from datetime import datetime, timezone
from .constants import *


def submit_correction(correction):
    correcteur = correction.correcteur
    exercice = correction.enonce
    posteur = exercice.posteur

    now = datetime.now(timezone.utc)
    condition = posteur != correcteur and \
                now <= exercice.date_limite and \
                exercice.correcs.count() == 1
    if condition:
        posteur.tirelire -= exercice.prix
        correcteur.tirelire += exercice.prix
    else:
        if posteur == correcteur:
            correcteur.tirelire += SELFCORREC_POINTS()
        elif now > exercice.date_limite:
            correcteur.tirelire += DEADLINE_POINTS()
        else:
            correcteur.tirelire += MULTIPLECORREC_POINTS()
    correcteur.unlocked_correcs.add(correction)
    posteur.unlocked_correcs.add(correction)
    posteur.save()
    correcteur.save()

    return True

def delete_correction(correction):
    correcteur = correction.correcteur
    exercice = correction.enonce
    posteur = exercice.posteur

    now = datetime.now(timezone.utc)
    condition = posteur != correcteur and \
                now <= exercice.date_limite and \
                exercice.correcs.count() == 1
    if condition:
        posteur.tirelire += exercice.prix
        correcteur.tirelire -= exercice.prix
    else:
        if posteur == correcteur:
            correcteur.tirelire -= SELFCORREC_POINTS()
        elif now > exercice.date_limite:
            correcteur.tirelire -= DEADLINE_POINTS()
        else:
            correcteur.tirelire -= MULTIPLECORREC_POINTS()
    correcteur.unlocked_correcs.remove(correction)
    posteur.unlocked_correcs.remove(correction)
    posteur.save()
    correcteur.save()

    return True


def buy_correction(user, correction):
    prix = correction.prix
    if user.tirelire >= prix:
        user.unlocked_correcs.add(correction)
        user.tirelire -= prix
        user.save()
        return True
    else:
        return False

