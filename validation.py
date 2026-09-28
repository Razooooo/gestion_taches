"""Contrôle des saisies. Chaque fonction retourne la valeur nettoyée,
ou lève ValueError avec un message compréhensible."""

from datetime import date

from models import STATUTS, PRIORITES


def valider_texte(valeur, nom_champ):
    """Un champ obligatoire ne doit pas être vide."""
    valeur = valeur.strip()
    if valeur == "":
        raise ValueError(f"Le champ '{nom_champ}' est obligatoire.")
    return valeur


def _normaliser(texte):
    """Minuscules, sans espaces autour, et sans accent sur le 'à' (pour taper 'a faire')."""
    return texte.strip().lower().replace("à", "a")


def _valider_dans_liste(valeur, valeurs_autorisees, nom_champ):
    """Cherche valeur dans la liste sans tenir compte de la casse ; retourne la forme officielle."""
    for autorisee in valeurs_autorisees:
        if _normaliser(valeur) == _normaliser(autorisee):
            return autorisee
    raise ValueError(
        f"{nom_champ} invalide : '{valeur}'. Valeurs autorisées : {', '.join(valeurs_autorisees)}."
    )


def valider_statut(valeur):
    return _valider_dans_liste(valeur, STATUTS, "Statut")


def valider_priorite(valeur):
    return _valider_dans_liste(valeur, PRIORITES, "Priorité")


def valider_date(valeur):
    """Vérifie le format AAAA-MM-JJ ET que la date existe (refuse 2026-02-30)."""
    valeur = valeur.strip()
    try:
        if len(valeur) != 10:  # Python 3.11+ accepte aussi "20260930" : on impose AAAA-MM-JJ
            raise ValueError
        date.fromisoformat(valeur)
    except ValueError:
        raise ValueError(f"Date invalide : '{valeur}'. Format attendu : AAAA-MM-JJ.")
    return valeur
