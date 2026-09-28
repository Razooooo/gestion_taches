"""Structure de données d'une tâche et valeurs autorisées."""

STATUTS = ["À faire", "En cours", "Terminée"]
PRIORITES = ["Basse", "Normale", "Haute"]


def nouvelle_tache(id, titre, description, responsable, priorite, statut, echeance):
    """Construit une tâche sous forme de dictionnaire (directement sérialisable en JSON)."""
    return {
        "id": id,
        "titre": titre,
        "description": description,
        "responsable": responsable,
        "priorite": priorite,
        "statut": statut,
        "echeance": echeance,  # texte au format ISO : "AAAA-MM-JJ"
    }
