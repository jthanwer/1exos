from datetime import datetime, timezone


def submit_correction(correction):
    correcteur = correction.correcteur
    exercice = correction.enonce
    posteur = exercice.posteur

    now = datetime.now(timezone.utc)
    condition = posteur != correcteur and \
                now < exercice.date_limite and \
                len(exercice.corrections.all()) == 1
    if condition:
        posteur.tirelire -= exercice.prix
        correcteur.tirelire += exercice.prix
    else:
        correcteur.tirelire += 3
    correcteur.correc.add(correction)
    posteur.correc.add(correction)
    posteur.save()
    correcteur.save()


def buy_correction(user, correction):
    prix = correction.prix
    if user.tirelire >= prix:
        user.correc.add(correction)
        user.tirelire -= prix
        user.save()
        return True
    else:
        return False

