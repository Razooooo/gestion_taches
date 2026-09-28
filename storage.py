"""Lecture / écriture du fichier JSON."""

import json
import os

DOSSIER = os.path.dirname(os.path.abspath(__file__))
CHEMIN_FICHIER = os.path.join(DOSSIER, "data", "taches.json")


def charger_taches(chemin=CHEMIN_FICHIER):
    """Retourne la liste des tâches. Ne plante jamais : liste vide si problème."""
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            taches = json.load(f)
    except FileNotFoundError:
        return []  # premier lancement : pas encore de fichier
    except ValueError:  # JSON invalide (JSONDecodeError est un ValueError)
        print(f"Attention : {chemin} est corrompu. Copie de sauvegarde créée.")
        os.replace(chemin, chemin + ".corrompu")  # on garde l'ancien fichier
        return []
    except OSError as erreur:
        print(f"Impossible de lire {chemin} : {erreur}")
        return []

    if not isinstance(taches, list):  # JSON valide mais pas une liste de tâches
        print(f"Attention : format inattendu dans {chemin}. Données ignorées.")
        return []
    return taches


def sauvegarder_taches(taches, chemin=CHEMIN_FICHIER):
    """Écrit la liste complète des tâches dans le fichier JSON."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(taches, f, indent=2, ensure_ascii=False)
