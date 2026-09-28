# Gestion de tâches (CLI Python)

Petit outil en ligne de commande pour suivre les tâches d'une équipe de développement :
titre, description, responsable, priorité, statut et échéance.

## Installation

- Python 3.10 ou plus récent.
- Aucune dépendance externe (bibliothèque standard uniquement) : il suffit de copier le dossier.

## Lancement

```
python main.py
```

Sous Windows, si `python` n'est pas reconnu, utiliser `py main.py`.

Tests :

```
python -m unittest discover tests
```

## Utilisation

Un menu numéroté s'affiche :

| Choix | Action |
|-------|--------|
| 1 | Lister les tâches (les tâches en retard sont signalées) |
| 2 | Afficher le détail d'une tâche (par id) |
| 3 | Créer une tâche (id automatique) |
| 4 | Modifier une tâche (Entrée = garder la valeur actuelle) |
| 5 | Supprimer une tâche (avec confirmation) |
| 6 | Rechercher un mot-clé dans le titre / la description |
| 7 | Filtrer par statut et/ou priorité |
| 8 | Statistiques : total, terminées, en retard |
| 0 | Quitter |

- Statuts : `À faire`, `En cours`, `Terminée` (la casse et l'accent sur « À » sont tolérés).
- Priorités : `Basse`, `Normale`, `Haute`.
- Dates au format `AAAA-MM-JJ`.
- Une tâche est « en retard » si elle n'est pas terminée et que son échéance est avant aujourd'hui.

## Choix techniques

- **JSON** (`data/taches.json`) : lisible et modifiable à la main, intégré à Python, largement suffisant pour
  quelques centaines de tâches. Le fichier est chargé au démarrage et réécrit après chaque modification.
- **CLI** : le sujet demande un outil simple ; un menu `input()` + boucle `while` est facile à tester et à relire.
- **Tâche = dictionnaire** : se convertit directement en JSON, sans classe ni conversion.
- **Validation avant modification** : si une saisie est invalide, une `ValueError` est levée et rien n'est changé.
- **Erreurs gérées** : fichier absent (liste vide), fichier corrompu (copié en `.corrompu`, on repart d'une liste vide),
  id inexistant (`TacheIntrouvable`), saisies invalides (message et nouvelle demande).

## Structure

```
main.py         menu CLI (affichage, saisies, appels aux autres modules)
models.py       statuts, priorités, construction d'une tâche
storage.py      lecture / écriture du JSON
validation.py   contrôle des saisies
operations.py   créer, modifier, supprimer, rechercher, filtrer (sur une liste en mémoire)
stats.py        total, terminées, en retard
data/           taches.json
tests/          test_operations.py
```

`operations.py` ne touche jamais au disque : c'est `main.py` qui sauvegarde. Cela rend les tests simples et rapides.
