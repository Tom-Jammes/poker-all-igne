from models.table import Table
from models.joueur import Joueur

class TestTable:
    def test_creation_table(self):
        nb_joueurs = 5
        montant_joueur = 500
        table = Table("Alice", nb_joueurs, montant_joueur)
        assert table.createur == "Alice"
        assert table.joueurs == []
        assert table.pot == 0
        assert table.petite_blind_index == (table.dealer_index + 1) % table.nb_joueurs
        assert table.grosse_blind_index == (table.dealer_index + 2) % table.nb_joueurs
        assert table.phase_jeu == "avant_premiere_donne"
        assert table.cartes_communes == []

    def test_ajouter_joueur(self):
        nb_joueurs = 5
        montant_joueur = 500
        table = Table("Bob", nb_joueurs, montant_joueur)
        joueur1 = Joueur("Charlie")
        joueur2 = Joueur("David")
        table.ajouter_joueur("Charlie")
        table.ajouter_joueur("David")
        assert joueur1 in table.joueurs
        assert joueur2 in table.joueurs
        assert table.joueurs[1].jetons == montant_joueur
        assert len(table.joueurs) == 2

    def test_ajouter_joueur_deja_present(self):
        nb_joueurs = 5
        montant_joueur = 500
        table = Table("Eve", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Frankie")
        table.ajouter_joueur("Frankie") # Ajouter le même joueur une deuxième fois
        assert len(table.joueurs) == 1

    def test_retirer_joueur(self):
        nb_joueurs = 5
        montant_joueur = 500
        table = Table("Grace", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Heidi")
        table.ajouter_joueur("Ivan")
        joueur1 = table.joueurs[0]
        joueur2 = table.joueurs[1]
        table.retirer_joueur(joueur1)
        assert joueur1 not in table.joueurs
        assert joueur2 in table.joueurs
        assert len(table.joueurs) == 1

    def test_retirer_joueur_non_present(self):
        nb_joueurs = 5
        montant_joueur = 500
        table = Table("Judy", nb_joueurs, montant_joueur)
        joueur = Joueur("Kelly", montant_joueur)
        table.retirer_joueur(joueur) # Tenter de retirer un joueur non présent
        assert len(table.joueurs) == 0 # ou l'état initial

    def test_demarrer_tour_pas_assez_de_joueurs(self):
        nb_joueurs = 5
        montant_joueur = 500
        table = Table("Liam", nb_joueurs, montant_joueur)
        assert table.demarrer_tour() is False
        table.ajouter_joueur("Mia")
        assert table.demarrer_tour() is False
        table.ajouter_joueur("Luca")
        assert table.demarrer_tour() is False
        table.ajouter_joueur("Axel")
        assert table.demarrer_tour() is False

    def test_demarrer_tour_pas_assez_de_jetons(self):
        nb_joueurs = 3
        montant_joueur = 5
        table = Table("Liam", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Liam")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")
        assert table.demarrer_tour() is True
        assert table.joueurs[table.petite_blind_index].all_in == True
        assert table.joueurs[table.grosse_blind_index].all_in == True

    def test_demarrer_tour_succes(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Noah", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Noah")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")
        assert table.demarrer_tour() is True
        croupier_debut = table.dealer_index
        petite_blind = table.petite_blind_index
        grosse_blind = table.grosse_blind_index
        assert table.paquet.nombre_de_cartes() == 52 - (len(table.joueurs) * 2) # 2 cartes par joueur
        assert table.pot == 30 # Les blinds sont payées
        assert table.mise_courante == 20
        assert table.phase_jeu == "premier_tour_mise"
        assert len(table.joueurs[0].main) == 2
        assert len(table.joueurs[1].main) == 2
        assert len(table.joueurs[2].main) == 2

        table.terminer_tour()
        table.demarrer_tour()
        assert table.grosse_blind_mise == 20
        assert table.petite_blind_mise == 10
        assert croupier_debut == (table.dealer_index -1) % nb_joueurs
        assert petite_blind == (table.petite_blind_index - 1) % nb_joueurs
        assert grosse_blind == (table.grosse_blind_index - 1) % nb_joueurs
        table.terminer_tour()
        table.demarrer_tour()
        assert table.grosse_blind_mise == 20
        assert table.petite_blind_mise == 10
        assert croupier_debut == (table.dealer_index - 2) % nb_joueurs
        assert petite_blind == (table.petite_blind_index - 2) % nb_joueurs
        assert grosse_blind == (table.grosse_blind_index - 2) % nb_joueurs
        table.terminer_tour()
        table.demarrer_tour()
        assert table.grosse_blind_mise == 20
        assert table.petite_blind_mise == 10
        table.terminer_tour()
        table.demarrer_tour()
        assert table.grosse_blind_mise == 20
        assert table.petite_blind_mise == 10
        table.terminer_tour()
        table.demarrer_tour()
        assert table.grosse_blind_mise == 40
        assert table.petite_blind_mise == 20

    def test_flop(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Nicolas", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Nicolas")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")

        assert table.demarrer_tour() is True
        assert table.flop() is True
        assert len(table.cartes_communes) == 3
        assert table.paquet.nombre_de_cartes() == 52 - (len(table.joueurs) * 2) - 6 # 3 cartes distribué commune + 3 cartes brulées
        assert table.phase_jeu == "deuxieme_tour_mise"

    def test_turn(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Nicolas", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Nicolas")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")

        assert table.demarrer_tour() is True
        assert table.turn() is False
        assert table.flop() is True
        assert table.turn() is True
        assert len(table.cartes_communes) == 4
        assert table.paquet.nombre_de_cartes() == 52 - (len(table.joueurs) * 2) - 8 # 4 cartes distribué commune + 4 cartes brulées
        assert table.phase_jeu == "troisieme_tour_mise"

    def test_river(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Nicolas", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Nicolas")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")

        assert table.demarrer_tour() is True
        assert table.flop() is True
        assert table.river() is False
        assert table.turn() is True
        assert table.river() is True
        assert len(table.cartes_communes) == 5
        assert table.paquet.nombre_de_cartes() == 52 - (len(table.joueurs) * 2) - 10 # 3 cartes distribué commune + 3 cartes brulées
        assert table.phase_jeu == "quatrieme_tour_mise"

    def test_terminer_tour(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Hugo", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Hugo")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")
        index_dealer_debut_partie = table.dealer_index

        assert table.phase_jeu == "avant_premiere_donne"
        assert table.petite_blind_index == (index_dealer_debut_partie + 1) % table.nb_joueurs
        assert table.grosse_blind_index == (index_dealer_debut_partie + 2) % table.nb_joueurs
        assert table.nb_tours == 0

        table.terminer_tour()
        assert table.phase_jeu == "fin_de_tour"
        assert table.dealer_index == (index_dealer_debut_partie + 1) % table.nb_joueurs
        assert table.petite_blind_index == (index_dealer_debut_partie + 2) % table.nb_joueurs
        assert table.grosse_blind_index == (index_dealer_debut_partie + 3) % table.nb_joueurs
        assert table.nb_tours == 1

    def test_actions_jeu(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Hugo", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Hugo")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")
        index_joueur_tour = table.index_joueur_tour

        assert table.joueur_action(table.joueurs[index_joueur_tour].nom,"se_couche") == False

        table.demarrer_tour()

        assert table.joueur_action(table.joueurs[(index_joueur_tour + 1) % table.nb_joueurs].nom, "se_couche") == False

        assert table.joueur_action(table.joueurs[index_joueur_tour].nom, "se_couche") == True
        assert table.joueur_action(table.joueurs[(index_joueur_tour + 1) % table.nb_joueurs].nom, "se_couche") == True
        assert table.joueur_action(table.joueurs[(index_joueur_tour + 2) % table.nb_joueurs].nom, "se_couche") == True

        assert table.joueur_action(table.joueurs[index_joueur_tour].nom, "se_couche") == False
        assert table.joueur_action(table.joueurs[table.petite_blind_index].nom, "se_couche") == True

    def test_tour_mise_suivant(self):
        nb_joueurs = 3
        montant_joueur = 500
        table = Table("Hugo", nb_joueurs, montant_joueur)
        table.ajouter_joueur("Hugo")
        table.ajouter_joueur("Olivia")
        table.ajouter_joueur("Peter")
        table.demarrer_tour()

        assert table.phase_jeu == "premier_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "premier_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "premier_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")

        assert table.phase_jeu == "deuxieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "deuxieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "deuxieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")

        assert table.phase_jeu == "troisieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "troisieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "troisieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")

        assert table.phase_jeu == "quatrieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "quatrieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")
        assert table.phase_jeu == "quatrieme_tour_mise"
        table.joueur_action(table.joueurs[table.index_joueur_tour].nom, "suit")

        assert table.phase_jeu == "fin_de_tour"
