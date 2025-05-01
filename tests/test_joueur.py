from models.joueur import Joueur
from models.cartes import Carte

class TestJoueur:
    def test_creation_joueur(self):
        joueur = Joueur("Alice", 1000)
        assert joueur.nom == "Alice"
        assert joueur.jetons == 1000
        assert joueur.main == []
        assert joueur.mise_courante == 0
        assert joueur.a_parle is False
        assert joueur.est_couche is False
        assert joueur.all_in is False

    def test_recevoir_carte(self):
        joueur = Joueur("Bob")
        carte1 = Carte(5, "Carreau")
        carte2 = Carte(12, "Trèfle")
        joueur.recevoir_carte(carte1)
        joueur.recevoir_carte(carte2)
        assert len(joueur.main) == 2
        assert joueur.main[0] == carte1
        assert joueur.main[1] == carte2

    def test_miser_succes(self):
        joueur = Joueur("Charlie", 500)
        assert joueur.miser(100) is True
        assert joueur.jetons == 400
        assert joueur.mise_courante == 100
        assert joueur.a_parle is True

    def test_miser_echec_pas_assez_jetons(self):
        joueur = Joueur("David", 50)
        assert joueur.miser(100) is False
        assert joueur.jetons == 50
        assert joueur.mise_courante == 0
        assert joueur.a_parle is False

    def test_miser_montant_negatif_ou_zero(self):
        joueur = Joueur("Eve", 200)
        assert joueur.miser(0) is False
        assert joueur.miser(-50) is False
        assert joueur.jetons == 200
        assert joueur.mise_courante == 0
        assert joueur.a_parle is False

    def test_suivre_succes(self):
        joueur = Joueur("Frankie", 300)
        joueur.mise_courante = 50
        assert joueur.suivre(100) is True
        assert joueur.jetons == 250
        assert joueur.mise_courante == 100
        assert joueur.a_parle is True

    def test_suivre_deja_mise_suffisamment(self):
        joueur = Joueur("Grace", 200)
        joueur.mise_courante = 100
        assert joueur.suivre(100) is True
        assert joueur.jetons == 200
        assert joueur.mise_courante == 100
        assert joueur.a_parle is True

    def test_suivre_echec_pas_assez_jetons(self):
        joueur = Joueur("Heidi", 50)
        joueur.mise_courante = 25
        assert joueur.suivre(100) is False
        assert joueur.jetons == 50
        assert joueur.mise_courante == 25
        assert joueur.a_parle is False

    def test_se_coucher(self):
        joueur = Joueur("Ivan")
        joueur.se_coucher()
        assert joueur.est_couche is True
        assert joueur.a_parle is True

    def test_aller_all_in(self):
        joueur = Joueur("Judy", 150)
        assert joueur.miser_all_in() is True
        assert joueur.all_in is True
        assert joueur.jetons == 0
        assert joueur.mise_courante == 150
        assert joueur.a_parle is True

    def test_aller_all_in_sans_jetons(self):
        joueur = Joueur("Kelly", 0)
        assert joueur.miser_all_in() is False
        assert joueur.all_in is False
        assert joueur.jetons == 0
        assert joueur.mise_courante == 0
        assert joueur.a_parle is False

    def test_reinitialiser_pour_nouveau_tour(self):
        joueur = Joueur("Liam", 200)
        joueur.recevoir_carte(Carte(3, "Pique"))
        joueur.se_coucher()
        joueur.miser_all_in()

        assert joueur.est_couche is True
        assert joueur.all_in is True

        joueur.reinitialiser_pour_nouveau_tour()
        assert joueur.main == []
        assert joueur.mise_courante == 0
        assert joueur.a_parle is False
        assert joueur.est_couche is False
        assert joueur.all_in is False
        assert joueur.jetons == 0 # Les jetons ne sont pas réinitialisés

    def test_representation_str_joueur(self):
        joueur = Joueur("Mia", 300)
        assert str(joueur) == "Joueur Mia (300 jetons)"

    def test_representation_repr_joueur(self):
        joueur = Joueur("Noah", 450)
        assert repr(joueur) == "Joueur(nom='Noah', jetons=450)"

    def test_eq(self):
        joueur1 = Joueur("Tom")
        joueur2 = Joueur("Raph")
        joueur3 = Joueur("Tom")

        assert joueur1 != joueur2
        assert joueur1 == joueur3