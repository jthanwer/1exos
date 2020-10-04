from datetime import datetime, timezone
import core.constants as cst


# ----------------------------
# -- Soumettre une correction
# ----------------------------
def submit_correction(correction):
    correcteur = correction.correcteur
    exercice = correction.enonce
    posteur = exercice.posteur

    now = datetime.now(timezone.utc)
    condition = posteur != correcteur and \
                now <= exercice.date_limite and \
                exercice.correcs.count() == 1

    # -- Si toutes les conditions sont réunies,
    # le prix du posteur est transféré
    if condition:
        posteur.tirelire -= exercice.prix
        correcteur.tirelire += exercice.prix
        correction.is_favorite = True
    # -- Sinon, applique un prix différent selon la situation
    else:
        if posteur == correcteur:
            correction.gain = cst.SELFCORREC_POINTS()
        elif now > exercice.date_limite:
            correction.gain = cst.DEADLINE_POINTS()
        else:
            correction.gain = cst.MULTIPLECORREC_POINTS()
        correcteur.tirelire += correction.gain
        correction.is_favorite = False

    # -- Sauvegarde les tirelires et la correction
    # -- Attention : bien laisser dans cet ordre
    posteur.save()
    correcteur.save()
    correction.save()

    # -- Débloque la correction pour toutes
    # les personnes qui ont déjà débloqué une correction ...
    all_corrections = correction.enonce.correcs.all()
    for elt in all_corrections:
        buyers = elt.buyers.all()
        for buyer in buyers:
            buyer.unlocked_correcs.add(correction)
        # ... sauf pour ceux qui n'ont fait que poster une correction
        elt.correcteur.unlocked_correcs.remove(correction)

    # -- Débloque la correction pour le correcteur
    correcteur.unlocked_correcs.add(correction)
    # -- Débloque la correction pour le posteur
    posteur.unlocked_correcs.add(correction)

    return True


# ----------------------------
# -- Supprimer une correction
# ----------------------------
def delete_correction(correction):
    correcteur = correction.correcteur
    exercice = correction.enonce
    posteur = exercice.posteur

    date_created = correction.date_created
    # -- Si la correction est la favorite
    # le prix proposé est retransféré
    # et une autre correction devient favorite
    if correction.is_favorite:
        correcteur.tirelire -= exercice.prix
        other_corrections = correction.enonce.correcs.exclude(id=correction.id).order_by('-date_created')
        at_least_one = False
        # -- On regarde les autres corrections
        if other_corrections.exists():
            for other_correction in other_corrections:
                date_created = other_correction.date_created
                other_correcteur = other_correction.correcteur
                condition = posteur != other_correcteur and \
                            date_created < exercice.date_limite
                # -- Si une autre correction peut être favorite,
                # on transfère les points à son correcteur
                if condition:
                    at_least_one = True
                    other_correction.is_favorite = True
                    other_correcteur.tirelire += (exercice.prix - other_correction.gain)
                    other_correction.gain = exercice.prix
                    other_correction.save()
                    other_correcteur.save()
                    break

            # -- Si aucune correctiion ne peut être favorite,
            # on rembourse le posteur
            if not at_least_one:
                posteur.tirelire += exercice.prix

        else:
            posteur.tirelire += exercice.prix

    # -- Sinon, retire les points gagnés
    else:
        if posteur == correcteur:
            correcteur.tirelire -= cst.SELFCORREC_POINTS()
        elif date_created > exercice.date_limite:
            correcteur.tirelire -= cst.DEADLINE_POINTS()
        else:
            correcteur.tirelire -= cst.MULTIPLECORREC_POINTS()

    # -- Si la correction était la seule disponible,
    # rembourse les acheteurs
    nb_corrections = correction.enonce.correcs.count()
    buyers = correction.buyers.all()
    if nb_corrections == 1:
        for buyer in buyers:
            if buyer != posteur and buyer != correcteur:
                buyer.tirelire += correction.prix
                buyer.save()

    # -- Sauvegarde les tirelires
    # -- Attention : bien laisser dans ce sens
    posteur.save()
    correcteur.save()

    # -- Enlève la correction pour le correcteur
    correcteur.unlocked_correcs.remove(correction)
    # -- Enlève la correction pour le posteur
    posteur.unlocked_correcs.remove(correction)

    return True


# ----------------------------
# -- Acheter une correction
# ----------------------------
def buy_correction(user, correction):
    prix = correction.prix
    # -- Si la cagnotte est suffisante en points
    if user.tirelire >= prix:
        user.unlocked_correcs.add(correction)
        user.tirelire -= prix
        user.save()
        return True
    else:
        return False
