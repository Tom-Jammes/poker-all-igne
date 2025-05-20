import random
from models.cartes import Paquet
from models.joueur import Joueur
from utils.evaluateur_main import EvaluateurDeMain


class Table:
    """Représente une table de poker."""
    def __init__(self, nom_createur, nb_joueurs, montant_joueurs):
        """
        Initialise une nouvelle table de poker.

        Args:
            nom_createur (str): le nom du joueur qui a créé la table de poker.
            nb_joueurs (int): nombre de joueurs pour la table de poker.
            montant_joueurs (int): montant de base par joueur.
        """
        self.createur = nom_createur
        self.nb_joueurs = nb_joueurs # nombre de joueurs pour lancer la table TODO définir un min à 3 et un max à 10
        self.joueurs = []  # Liste des objets Joueur assis à la table
        self.gagnant = []
        self.combinaison_gagnante = []
        self.paquet = None
        self.pot = 0
        self.montant_joueurs = montant_joueurs
        self.dealer_index = random.randint(0, nb_joueurs-1)  # Index du joueur qui est le croupier actuel
        self.petite_blind_index = (self.dealer_index + 1) % nb_joueurs  # Index du joueur pour la petite blind
        self.grosse_blind_index = (self.dealer_index + 2) % nb_joueurs  # Index du joueur pour la grosse blind
        self.index_joueur_tour = (self.dealer_index + 3) % nb_joueurs
        self.petite_blind_mise = 10
        self.grosse_blind_mise = 20
        self.mise_courante = 0  # La mise actuelle à égaler pour rester dans le tour
        self.dernier_a_relancer = None  # Le joueur qui a fait la dernière relance
        self.phase_jeu = "avant_premiere_donne"  # État actuel du jeu (avant_premiere_donne, premiere_donne, flop, turn, river, fin_de_tour)
        self.cartes_communes = []  # Les cartes au centre de la table
        self.historique_actions = [] # Liste des actions effectuées pendant le tour
        self.nb_tours = 0
        print(f"Table créée par {self.createur}.")

    def ajouter_joueur(self, nom_joueur):
        """
        Ajoute un joueur à la table.
        Args:
            nom_joueur (str): nom du joueur qui rejoint la table
        """
        joueur = Joueur(nom_joueur, self.montant_joueurs)
        if joueur not in self.joueurs:
            self.joueurs.append(joueur)
            print(f"{joueur.nom} a rejoint la table.")
            self._mettre_a_jour_indices_blinds() # Mettre à jour les blinds si nécessaire
        else:
            print(f"{joueur.nom} est déjà à la table.")

    def retirer_joueur(self, joueur):
        """Retire un joueur de la table."""
        if joueur in self.joueurs:
            self.joueurs.remove(joueur)
            print(f"{joueur.nom} a quitté la table.")
            self._mettre_a_jour_indices_blinds() # Mettre à jour les blinds si nécessaire
        else:
            print(f"{joueur.nom} n'est pas à la table.")

    def _mettre_a_jour_indices_blinds(self):
        """Met à jour les indices des blinds et du joueur_tour en fonction du nombre de joueurs."""
        nombre_joueurs = len(self.joueurs)
        if nombre_joueurs >= 2:
            if nombre_joueurs > 2:
                self.petite_blind_index = (self.dealer_index + 1) % nombre_joueurs
            else:
                # En heads-up, le dealer est la petite blind, l'autre la grosse
                self.petite_blind_index = self.dealer_index
        self.grosse_blind_index = (self.petite_blind_index + 1) % nombre_joueurs
        self.index_joueur_tour = (self.grosse_blind_index + 1) % nombre_joueurs

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
        self.gagnant = []
        self.combinaison_gagnante = []
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
                petite_blind_joueur.a_parle = False
                self.pot += self.petite_blind_mise
                self.mise_courante = max(self.mise_courante, self.petite_blind_mise)
                self.historique_actions.append(f"{petite_blind_joueur.nom} paie la petite blind ({self.petite_blind_mise})")
            else:
                petite_blind_joueur.miser_all_in()
                print(f"Erreur : {petite_blind_joueur.nom} a du all-in pour payer la petite blind.")

            print(f"{grosse_blind_joueur.nom} paie la grosse blind de {self.grosse_blind_mise}.")
            if grosse_blind_joueur.miser(self.grosse_blind_mise):
                grosse_blind_joueur.a_parle = False
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
        joueurs_en_jeu = [joueur for joueur in self.joueurs if not joueur.est_couche]

        if len(joueurs_en_jeu) == 1:
            gagnant = joueurs_en_jeu[0]
            gagnant.jetons += self.pot
            print(f"\n{gagnant.nom} remporte le pot de {self.pot} jetons.")
            self.gagnant = [gagnant]
        elif len(joueurs_en_jeu) > 1:
            gagnant = []
            evaluateur = EvaluateurDeMain()
            meilleur_score = 0
            combinaison_gagnante = []
            for joueur in joueurs_en_jeu:
                score,combinaison = evaluateur.evaluer_main_7_cartes(joueur.main + self.cartes_communes)
                if score > meilleur_score:
                    meilleur_score = score
                    combinaison_gagnante = combinaison
                    gagnant = [joueur]
                elif score == meilleur_score:
                    gagnant.append(joueur)

            for joueur in gagnant:
                joueur.jetons += self.pot / len(gagnant)

            if len(gagnant) > 1:
                print(f"\n{len(gagnant)} gagants remportent le pot de {self.pot/len(gagnant)} jetons chacun.")
            else:
                print(f"\n{gagnant[0].nom} remporte le pot de {self.pot} jetons.")
            self.gagnant = gagnant
            self.combinaison_gagnante = combinaison_gagnante

    def terminer_tour(self):
        """Termine le tour actuel."""
        print("\n--- Fin du tour ---")
        self._determiner_gagnant()
        self._avancer_dealer()
        self.phase_jeu = "fin_de_tour"
        self.nb_tours += 1

    def joueur_action(self, nom_joueur, action):
        """
        Effectue l'action d'un joueur
        :param
            nom_joueur (str): nom du joueur qui effectue l'action
        :return: True si le joueur a pu effectuer l'action, False sinon
        """
        if nom_joueur != self.joueurs[self.index_joueur_tour].nom or self.phase_jeu == "avant_premiere_donne":
            return False

        print(f"{nom_joueur} {action}")
        self.joueurs[self.index_joueur_tour].a_parle = True

        if self._est_tous_joueurs_ont_parle(): # On passe au tour suivant de mise
            self._tour_suivant_mise()
        else: # On continue le tour
            self.index_joueur_tour = (self.index_joueur_tour + 1) % len(self.joueurs) # TODO gérer le cas où le joueur suivant est couché ou all-in

        return True

    def _est_tous_joueurs_ont_parle(self):
        for joueur in self.joueurs:
            if not joueur.a_parle:
                return False
        return True

    def _tour_suivant_mise(self):
        if self.flop() or self.turn() or self.river():
            for joueur in self.joueurs:
                joueur.a_parle = False
            self.index_joueur_tour = self.petite_blind_index # TODO gérer le cas où le joueur est couché ou all-in
        else:
            self.terminer_tour()


    def __str__(self):
        return (f"Table de poker créée par {self.createur}, ({len(self.joueurs)} joueurs), {self.montant_joueurs} jetons par joueurs"
                f"{self.joueurs} joueurs dans la table actuellement")

    def __repr__(self):
        return f"Table(createur='{self.createur}', joueurs={[j.nom for j in self.joueurs]}, montant_joueurs={self.montant_joueurs})"