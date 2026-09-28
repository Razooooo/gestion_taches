"""Opérations sur la liste de tâches : créer, modifier, supprimer, rechercher, filtrer.
Ces fonctions travaillent sur une liste en mémoire ; la sauvegarde est faite par main.py."""

import validation
from models import nouvelle_tache


class TacheIntrouvable(Exception):
    """Levée quand aucun id ne correspond."""


def trouver_tache(taches, id_tache):
    for tache in taches:
        if tache["id"] == id_tache:
            return tache
    raise TacheIntrouvable(f"Aucune tâche avec l'id {id_tache}.")


def creer_tache(taches, titre, description, responsable, priorite, statut, echeance):
    # On valide tout AVANT de toucher à la liste : si une erreur survient, rien n'est ajouté.
    titre = validation.valider_texte(titre, "titre")
    description = validation.valider_texte(description, "description")
    responsable = validation.valider_texte(responsable, "responsable")
    priorite = validation.valider_priorite(priorite)
    statut = validation.valider_statut(statut)
    echeance = validation.valider_date(echeance)

    nouvel_id = max((t["id"] for t in taches), default=0) + 1  # plus grand id + 1
    tache = nouvelle_tache(nouvel_id, titre, description, responsable, priorite, statut, echeance)
    taches.append(tache)
    return tache


def modifier_tache(taches, id_tache, **champs):
    """Modifie les champs donnés (ex : statut="Terminée"). Les champs à None sont ignorés."""
    tache = trouver_tache(taches, id_tache)

    validateurs = {
        "titre": lambda v: validation.valider_texte(v, "titre"),
        "description": lambda v: validation.valider_texte(v, "description"),
        "responsable": lambda v: validation.valider_texte(v, "responsable"),
        "priorite": validation.valider_priorite,
        "statut": validation.valider_statut,
        "echeance": validation.valider_date,
    }

    # 1) on valide tout dans un dictionnaire temporaire ; 2) on applique seulement si tout est bon
    nouvelles_valeurs = {}
    for nom, valeur in champs.items():
        if valeur is None:
            continue
        if nom not in validateurs:
            raise ValueError(f"Champ inconnu : '{nom}'.")
        nouvelles_valeurs[nom] = validateurs[nom](valeur)

    tache.update(nouvelles_valeurs)
    return tache


def supprimer_tache(taches, id_tache):
    tache = trouver_tache(taches, id_tache)
    taches.remove(tache)
    return tache


def rechercher(taches, mot_cle):
    """Tâches dont le titre ou la description contient le mot-clé (sans tenir compte de la casse)."""
    mot_cle = mot_cle.strip().lower()
    return [
        t for t in taches
        if mot_cle in t["titre"].lower() or mot_cle in t["description"].lower()
    ]


def filtrer(taches, statut=None, priorite=None):
    """Filtre par statut et/ou priorité (un critère à None est ignoré)."""
    resultat = taches
    if statut is not None:
        statut = validation.valider_statut(statut)
        resultat = [t for t in resultat if t["statut"] == statut]
    if priorite is not None:
        priorite = validation.valider_priorite(priorite)
        resultat = [t for t in resultat if t["priorite"] == priorite]
    return resultat
