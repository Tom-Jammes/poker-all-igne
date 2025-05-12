import random
from models.cartes import Paquet
from models.joueur import Joueur

class Table:
    """Représente une table de poker."""
    def __init__(self, code, nom_createur, nb_joueurs, montant_joueurs):
        """
        Initialise une nouvelle table de poker.

        Args:
            code: Un code unique pour identifier la table.
            nom_createur (str): le nom du joueur qui a créé la table de poker.
            nb_joueurs (int): nombre de joueurs pour la table de poker.
            montant_joueurs (int): montant de base par joueur.
        """
        self.code = code
        self.createur = Joueur(nom_createur, montant_joueurs)
        self.nb_joueurs = nb_joueurs # TODO définir un min à 3 et un max à 10
        self.joueurs = [self.createur]  # Liste des objets Joueur assis à la table
        self.paquet = None
        self.pot = 0
        self.montant_joueurs = montant_joueurs
        self.dealer_index = 0  # Index du joueur qui est le croupier actuel
        self.petite_blind_index = 1  # Index du joueur pour la petite blind
        self.grosse_blind_index = 2  # Index du joueur pour la grosse blind
        self.petite_blind_mise = 10
        self.grosse_blind_mise = 20
        self.mise_courante = 0  # La mise actuelle à égaler pour rester dans le tour
        self.dernier_a_relancer = None  # Le joueur qui a fait la dernière relance
        self.phase_jeu = "avant_premiere_donne"  # État actuel du jeu (avant_premiere_donne, premiere_donne, flop, turn, river, fin_de_tour)
        self.cartes_communes = []  # Les cartes au centre de la table
        self.historique_actions = [] # Liste des actions effectuées pendant le tour
        self.nb_tours = 0
        print(f"Table '{self.code}' créée par {self.createur}.")

    def ajouter_joueur(self, nom_joueur):
        """
        Ajoute un joueur à la table.
        Args:
            nom_joueur (str): nom du joueur qui rejoint la table
        """
        joueur = Joueur(nom_joueur, self.montant_joueurs)
        if joueur not in self.joueurs:
            self.joueurs.append(joueur)
            print(f"{joueur.nom} a rejoint la table '{self.code}'.")
            self._mettre_a_jour_indices_blinds() # Mettre à jour les blinds si nécessaire
        else:
            print(f"{joueur.nom} est déjà à la table '{self.code}'.")

    def retirer_joueur(self, joueur):
        """Retire un joueur de la table."""
        if joueur in self.joueurs:
            self.joueurs.remove(joueur)
            print(f"{joueur.nom} a quitté la table '{self.code}'.")
            self._mettre_a_jour_indices_blinds() # Mettre à jour les blinds si nécessaire
        else:
            print(f"{joueur.nom} n'est pas à la table '{self.code}'.")

    def _mettre_a_jour_indices_blinds(self):
        """Met à jour les indices du croupier et des blinds en fonction du nombre de joueurs."""
        nombre_joueurs = len(self.joueurs)
        if nombre_joueurs >= 2:
            self.petite_blind_index = (self.dealer_index + 1) % nombre_joueurs
            if nombre_joueurs > 2:
                self.grosse_blind_index = (self.dealer_index + 2) % nombre_joueurs
            else:
                # En heads-up, le dealer est la petite blind, l'autre la grosse
                self.grosse_blind_index = self.dealer_index ^ 1 # XOR avec 1 pour obtenir l'autre index

    def demarrer_tour(self):
        """Démarre un nouveau tour de poker."""
        if len(self.joueurs) < self.nb_joueurs:
            print("Pas assez de joueurs pour démarrer un tour.")
            return False

        if self.nb_tours != 0 and self.nb_tours % 5 == 0 : # On augmente la blind au fur et à mesure
            self.petite_blind_mise += 10
            self.grosse_blind_mise += 20

        print(f"\n--- Début du tour ---")
        self.paquet = Paquet()
        self.paquet.melanger()
        self.pot = 0
        self.mise_courante = 0
        self.dernier_a_relancer = None
        self.phase_jeu = "premiere_donne"
        self.cartes_communes = []
        self.historique_actions = []

        # Réinitialiser l'état des joueurs pour le nouveau tour
        for joueur in self.joueurs:
            joueur.reinitialiser_pour_nouveau_tour()

        self._distribuer_cartes_initiales()
        self._payer_blinds()
        self.phase_jeu = "premier_tour_mise"
        self._afficher_etat_table()
        return True

    def _distribuer_cartes_initiales(self):
        """Distribue deux cartes à chaque joueur."""
        for _ in range(2):
            for joueur in self.joueurs:
                carte = self.paquet.tirer_carte()
                if carte:
                    joueur.recevoir_carte(carte)
                else:
                    print("Erreur : Paquet vide pendant la distribution initiale.")
                    return

        for joueur in self.joueurs:
            joueur.afficher_main() # Les autres joueurs ne voient pas les mains

    def _payer_blinds(self):
        """Fait payer la petite et la grosse blind."""
        nombre_joueurs = len(self.joueurs)
        if nombre_joueurs >= 2:
            petite_blind_joueur = self.joueurs[self.petite_blind_index % nombre_joueurs]
            grosse_blind_joueur = self.joueurs[self.grosse_blind_index % nombre_joueurs]

            print(f"{petite_blind_joueur.nom} paie la petite blind de {self.petite_blind_mise}.")
            if petite_blind_joueur.miser(self.petite_blind_mise):
                self.pot += self.petite_blind_mise
                self.mise_courante = max(self.mise_courante, self.petite_blind_mise)
                self.historique_actions.append(f"{petite_blind_joueur.nom} paie la petite blind ({self.petite_blind_mise})")
            else:
                petite_blind_joueur.miser_all_in()
                print(f"Erreur : {petite_blind_joueur.nom} a du all-in pour payer la petite blind.")

            print(f"{grosse_blind_joueur.nom} paie la grosse blind de {self.grosse_blind_mise}.")
            if grosse_blind_joueur.miser(self.grosse_blind_mise):
                self.pot += self.grosse_blind_mise
                self.mise_courante = max(self.mise_courante, self.grosse_blind_mise)
                self.dernier_a_relancer = grosse_blind_joueur
                self.historique_actions.append(f"{grosse_blind_joueur.nom} paie la grosse blind ({self.grosse_blind_mise})")
            else:
                grosse_blind_joueur.miser_all_in()
                print(f"Erreur : {grosse_blind_joueur.nom} a du all-in pour payer la grosse blind.")

    def _distribuer_cartes_communes(self, nombre):
        """Distribue un certain nombre de cartes communes."""
        for _ in range(nombre):
            # Brûler une carte avant de distribuer (règle du poker)
            if self.paquet.nombre_de_cartes() > 0:
                self.paquet.tirer_carte()
            carte = self.paquet.tirer_carte()
            if carte:
                self.cartes_communes.append(carte)
                print(f"Carte commune : {carte}")
            else:
                print("Erreur : Paquet vide lors de la distribution des cartes communes.")
                return

    def flop(self):
        """Distribue les trois premières cartes communes (le flop)."""
        if self.phase_jeu == "premier_tour_mise":
            print("\n--- Le Flop ---")
            self._distribuer_cartes_communes(3)
            self.phase_jeu = "deuxieme_tour_mise"
            self._afficher_etat_table()
            return True
        else:
            print("Impossible de passer au flop.")
            return False

    def turn(self):
        """Distribue la quatrième carte commune (le turn)."""
        if self.phase_jeu == "deuxieme_tour_mise":
            print("\n--- Le Turn ---")
            self._distribuer_cartes_communes(1)
            self.phase_jeu = "troisieme_tour_mise"
            self._afficher_etat_table()
            return True
        else:
            print("Impossible de passer au turn.")
            return False

    def river(self):
        """Distribue la cinquième et dernière carte commune (la river)."""
        if self.phase_jeu == "troisieme_tour_mise":
            print("\n--- La River ---")
            self._distribuer_cartes_communes(1)
            self.phase_jeu = "quatrieme_tour_mise"
            self._afficher_etat_table()
            return True
        else:
            print("Impossible de passer à la river.")
            return False

    def _afficher_etat_table(self):
        """Affiche l'état actuel de la table."""
        print(f"Pot : {self.pot} jetons")
        print("Cartes communes :", [str(carte) for carte in self.cartes_communes])
        for joueur in self.joueurs:
            print(f"{joueur.nom} (mise: {joueur.mise_courante}, jetons: {joueur.jetons}, {'couché' if joueur.est_couche else 'en jeu'})")

    def _avancer_dealer(self):
        """Passe le rôle du croupier au joueur suivant."""
        self.dealer_index = (self.dealer_index + 1) % len(self.joueurs)
        self._mettre_a_jour_indices_blinds()
        print(f"\nLe croupier est maintenant {self.joueurs[self.dealer_index].nom}.")

    def _determiner_gagnant(self):
        """Determine quel joueur gagne le tour"""
        joueurs_en_jeu = [joueur for joueur in self.joueurs if not joueur.est_couche and not joueur.all_in]
        if not joueurs_en_jeu:
            joueurs_en_jeu = [joueur for joueur in self.joueurs if not joueur.est_couche] # Si tout le monde à tapis

        if len(joueurs_en_jeu) == 1:
            gagnant = joueurs_en_jeu[0]
            gagnant.jetons += self.pot
            print(f"\n{gagnant.nom} remporte le pot de {self.pot} jetons.")
            return [gagnant]
        elif len(joueurs_en_jeu) > 1:
            # TODO Logique d'évaluation des mains à implémenter ici
            gagnant = random.choice(joueurs_en_jeu) # Choix aléatoire pour l'instant
            gagnant.jetons += self.pot
            print(f"\n{gagnant.nom} (aléatoirement) remporte le pot de {self.pot} jetons.")
            return [gagnant]
        else:
            print("\nPas de gagnant (tous les joueurs se sont couchés ?). Le pot est conservé pour le prochain tour.")
            return []

    def terminer_tour(self):
        """Termine le tour actuel."""
        print("\n--- Fin du tour ---")
        self._determiner_gagnant()
        self._avancer_dealer()
        self.phase_jeu = "fin_de_tour"
        self.nb_tours += 1

    def __str__(self):
        return f"Table de poker '{self.code}' créée par {self.createur} ({len(self.joueurs)} joueurs)"

    def __repr__(self):
        return f"Table(code='{self.code}', createur='{self.createur}', joueurs={[j.nom for j in self.joueurs]})"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TableModel(db.Model):
    __tablename__ = 'tables_poker'

    id = db.Column(db.Integer, primary_key=True)
    nombre_joueurs = db.Column(db.Integer, nullable=False)
    createur = db.Column(db.String(80), nullable=False)
    montant_joueurs = db.Column(db.Integer, nullable=False)
    date_creation = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, nombre_joueurs, createur, montant_joueurs):
        self.nombre_joueurs = nombre_joueurs
        self.montant_joueurs = montant_joueurs
        self.createur = createur

    def __repr__(self):
        return f"<Table {self.id}, nombre_joueurs: {self.nombre_joueurs}, createur: {self.createur}, montant_joueurs: {self.montant_joueurs}, date_creation: {self.date_creation}>"