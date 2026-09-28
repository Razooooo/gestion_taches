"""Point d'entrée : menu en ligne de commande."""

import operations
import stats
import storage
import validation
from models import STATUTS, PRIORITES
from operations import TacheIntrouvable


# ---------- Utilitaires d'affichage et de saisie ----------

def afficher_ligne(tache):
    retard = "  [EN RETARD]" if stats.est_en_retard(tache) else ""
    print(f"[{tache['id']}] {tache['titre']} | {tache['responsable']} | "
          f"{tache['priorite']} | {tache['statut']} | {tache['echeance']}{retard}")


def afficher_liste(taches):
    if not taches:
        print("Aucune tâche.")
        return
    for tache in taches:
        afficher_ligne(tache)


def afficher_detail(tache):
    print(f"Id          : {tache['id']}")
    print(f"Titre       : {tache['titre']}")
    print(f"Description : {tache['description']}")
    print(f"Responsable : {tache['responsable']}")
    print(f"Priorité    : {tache['priorite']}")
    print(f"Statut      : {tache['statut']}")
    print(f"Échéance    : {tache['echeance']}")


def demander(message, validateur, optionnel=False):
    """Redemande la saisie tant qu'elle est invalide.
    Si optionnel=True, une saisie vide retourne None (= ne pas changer / ne pas filtrer)."""
    while True:
        saisie = input(message).strip()
        if optionnel and saisie == "":
            return None
        try:
            return validateur(saisie)
        except ValueError as erreur:
            print("Erreur :", erreur)


def demander_id():
    """Retourne un entier, ou None si la saisie n'est pas un nombre."""
    try:
        return int(input("Id de la tâche : "))
    except ValueError:
        print("Erreur : l'id doit être un nombre entier.")
        return None


def sauvegarder(taches):
    try:
        storage.sauvegarder_taches(taches)
    except OSError as erreur:
        print("Erreur : sauvegarde impossible :", erreur)


# ---------- Actions du menu ----------

def action_creer(taches):
    titre = demander("Titre : ", lambda v: validation.valider_texte(v, "titre"))
    description = demander("Description : ", lambda v: validation.valider_texte(v, "description"))
    responsable = demander("Responsable : ", lambda v: validation.valider_texte(v, "responsable"))
    priorite = demander(f"Priorité ({'/'.join(PRIORITES)}) : ", validation.valider_priorite)
    statut = demander(f"Statut ({'/'.join(STATUTS)}) : ", validation.valider_statut)
    echeance = demander("Échéance (AAAA-MM-JJ) : ", validation.valider_date)

    tache = operations.creer_tache(taches, titre, description, responsable,
                                   priorite, statut, echeance)
    sauvegarder(taches)
    print(f"Tâche {tache['id']} créée.")


def action_detail(taches):
    id_tache = demander_id()
    if id_tache is None:
        return
    afficher_detail(operations.trouver_tache(taches, id_tache))


def action_modifier(taches):
    id_tache = demander_id()
    if id_tache is None:
        return
    tache = operations.trouver_tache(taches, id_tache)  # échoue tout de suite si id inconnu
    afficher_detail(tache)
    print("Appuyez sur Entrée pour garder la valeur actuelle.")

    titre = demander("Nouveau titre : ", lambda v: validation.valider_texte(v, "titre"), optionnel=True)
    description = demander("Nouvelle description : ", lambda v: validation.valider_texte(v, "description"), optionnel=True)
    responsable = demander("Nouveau responsable : ", lambda v: validation.valider_texte(v, "responsable"), optionnel=True)
    priorite = demander(f"Nouvelle priorité ({'/'.join(PRIORITES)}) : ", validation.valider_priorite, optionnel=True)
    statut = demander(f"Nouveau statut ({'/'.join(STATUTS)}) : ", validation.valider_statut, optionnel=True)
    echeance = demander("Nouvelle échéance (AAAA-MM-JJ) : ", validation.valider_date, optionnel=True)

    operations.modifier_tache(taches, id_tache, titre=titre, description=description,
                              responsable=responsable, priorite=priorite,
                              statut=statut, echeance=echeance)
    sauvegarder(taches)
    print("Tâche modifiée.")


def action_supprimer(taches):
    id_tache = demander_id()
    if id_tache is None:
        return
    tache = operations.trouver_tache(taches, id_tache)
    afficher_ligne(tache)
    if input("Confirmer la suppression ? (o/n) : ").strip().lower() != "o":
        print("Suppression annulée.")
        return
    operations.supprimer_tache(taches, id_tache)
    sauvegarder(taches)
    print("Tâche supprimée.")


def action_rechercher(taches):
    mot_cle = input("Mot-clé : ")
    afficher_liste(operations.rechercher(taches, mot_cle))


def action_filtrer(taches):
    statut = demander(f"Statut ({'/'.join(STATUTS)}, Entrée = tous) : ",
                      validation.valider_statut, optionnel=True)
    priorite = demander(f"Priorité ({'/'.join(PRIORITES)}, Entrée = toutes) : ",
                        validation.valider_priorite, optionnel=True)
    afficher_liste(operations.filtrer(taches, statut, priorite))


def action_stats(taches):
    resultat = stats.calculer_stats(taches)
    print(f"Total des tâches : {resultat['total']}")
    print(f"Tâches terminées : {resultat['terminees']}")
    print(f"Tâches en retard : {resultat['en_retard']}")


# ---------- Menu principal ----------

MENU = """
===== Gestion de tâches =====
1. Lister les tâches
2. Détail d'une tâche
3. Créer une tâche
4. Modifier une tâche
5. Supprimer une tâche
6. Rechercher par mot-clé
7. Filtrer par statut / priorité
8. Statistiques
0. Quitter"""


def main():
    taches = storage.charger_taches()

    while True:
        print(MENU)
        choix = input("Votre choix : ").strip()
        try:
            if choix == "1":
                afficher_liste(taches)
            elif choix == "2":
                action_detail(taches)
            elif choix == "3":
                action_creer(taches)
            elif choix == "4":
                action_modifier(taches)
            elif choix == "5":
                action_supprimer(taches)
            elif choix == "6":
                action_rechercher(taches)
            elif choix == "7":
                action_filtrer(taches)
            elif choix == "8":
                action_stats(taches)
            elif choix == "0":
                print("Au revoir.")
                break
            else:
                print("Choix invalide.")
        except TacheIntrouvable as erreur:
            print("Erreur :", erreur)
        except ValueError as erreur:
            print("Erreur :", erreur)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInterruption. Au revoir.")
