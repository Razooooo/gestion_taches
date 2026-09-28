"""Indicateurs : total, terminées, en retard."""

from datetime import date


def est_en_retard(tache, aujourdhui=None):
    """En retard = pas terminée ET échéance strictement avant aujourd'hui."""
    if aujourdhui is None:
        aujourdhui = date.today()
    if tache["statut"] == "Terminée":
        return False
    try:
        return date.fromisoformat(tache["echeance"]) < aujourdhui
    except (KeyError, ValueError):  # date absente/illisible (JSON modifié à la main)
        return False


def calculer_stats(taches, aujourdhui=None):
    return {
        "total": len(taches),
        "terminees": len([t for t in taches if t["statut"] == "Terminée"]),
        "en_retard": len([t for t in taches if est_en_retard(t, aujourdhui)]),
    }
