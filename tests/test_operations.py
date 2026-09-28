import os
import sys
import tempfile
import unittest

# permet d'importer les modules du dossier parent, quel que soit l'endroit d'où on lance les tests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import operations
import stats
import storage
from datetime import date
from operations import TacheIntrouvable


def tache_exemple(taches, titre="Corriger le bug de login", **autres):
    """Crée une tâche valide dans la liste `taches` (les valeurs peuvent être surchargées)."""
    valeurs = dict(description="Erreur 500 à la connexion", responsable="Alice",
                   priorite="Haute", statut="En cours", echeance="2026-09-30")
    valeurs.update(autres)
    return operations.creer_tache(taches, titre, **valeurs)


class TestOperations(unittest.TestCase):

    def setUp(self):
        self.taches = []  # liste vide neuve avant chaque test

    def test_creation_valide(self):
        tache = tache_exemple(self.taches)
        self.assertEqual(tache["id"], 1)
        self.assertEqual(len(self.taches), 1)
        self.assertEqual(tache_exemple(self.taches, "Autre")["id"], 2)  # auto-incrément

    def test_modification(self):
        tache = tache_exemple(self.taches)
        operations.modifier_tache(self.taches, tache["id"], statut="terminée", responsable="Bob")
        self.assertEqual(self.taches[0]["statut"], "Terminée")  # normalisé
        self.assertEqual(self.taches[0]["responsable"], "Bob")

    def test_recherche_insensible_a_la_casse(self):
        tache_exemple(self.taches, "Corriger le BUG de login")
        tache_exemple(self.taches, "Écrire la doc", description="README")
        self.assertEqual(len(operations.rechercher(self.taches, "bug")), 1)
        self.assertEqual(len(operations.rechercher(self.taches, "readme")), 1)
        self.assertEqual(operations.rechercher(self.taches, "inexistant"), [])

    def test_filtre_statut_et_priorite(self):
        tache_exemple(self.taches, "A", statut="À faire", priorite="Basse")
        tache_exemple(self.taches, "B", statut="À faire", priorite="Haute")
        self.assertEqual(len(operations.filtrer(self.taches, statut="À faire")), 2)
        self.assertEqual(len(operations.filtrer(self.taches, statut="À faire", priorite="Haute")), 1)

    def test_suppression(self):
        tache = tache_exemple(self.taches)
        operations.supprimer_tache(self.taches, tache["id"])
        self.assertEqual(self.taches, [])

    def test_erreur_id_inexistant(self):
        with self.assertRaises(TacheIntrouvable):
            operations.supprimer_tache(self.taches, 99)
        with self.assertRaises(TacheIntrouvable):
            operations.modifier_tache(self.taches, 99, statut="En cours")

    def test_erreur_saisie_invalide(self):
        with self.assertRaises(ValueError):
            tache_exemple(self.taches, priorite="Urgente")
        with self.assertRaises(ValueError):
            tache_exemple(self.taches, statut="Fini")
        with self.assertRaises(ValueError):
            tache_exemple(self.taches, echeance="2026-02-30")
        with self.assertRaises(ValueError):
            tache_exemple(self.taches, titre="   ")
        self.assertEqual(self.taches, [])  # rien n'a été ajouté

    def test_modification_invalide_ne_change_rien(self):
        tache = tache_exemple(self.taches)
        with self.assertRaises(ValueError):
            operations.modifier_tache(self.taches, tache["id"], responsable="Bob", priorite="???")
        self.assertEqual(self.taches[0]["responsable"], "Alice")


class TestStats(unittest.TestCase):

    def test_total_terminees_en_retard(self):
        taches = []
        tache_exemple(taches, "Retard", echeance="2026-01-01", statut="En cours")
        tache_exemple(taches, "Finie en retard", echeance="2026-01-01", statut="Terminée")
        tache_exemple(taches, "Futur", echeance="2026-12-31", statut="À faire")
        resultat = stats.calculer_stats(taches, aujourdhui=date(2026, 6, 1))
        self.assertEqual(resultat, {"total": 3, "terminees": 1, "en_retard": 1})


class TestStorage(unittest.TestCase):

    def test_sauvegarde_puis_chargement(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "taches.json")
            taches = []
            tache_exemple(taches)
            storage.sauvegarder_taches(taches, chemin)
            self.assertEqual(storage.charger_taches(chemin), taches)

    def test_fichier_absent_ou_corrompu(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "taches.json")
            self.assertEqual(storage.charger_taches(chemin), [])  # absent
            with open(chemin, "w", encoding="utf-8") as f:
                f.write("{ pas du json")
            self.assertEqual(storage.charger_taches(chemin), [])  # corrompu : pas de crash


if __name__ == "__main__":
    unittest.main()
