class Joueur:
    """Représente un joueur dans la partie de poker."""
    def __init__(self, nom, jetons=0):
        """
        Initialise un nouveau joueur.

        Args:
            nom (str): Le nom du joueur.
            jetons (int, optional): Le nombre de jetons avec lequel le joueur commence. Par défaut à 0.
        """
        self.nom = nom
        self.jetons = jetons
        self.main = []  # Liste pour stocker les cartes en main du joueur
        self.mise_courante = 0  # Montant misé par le joueur dans le tour actuel
        self.a_parle = False  # Indique si le joueur a déjà agi dans le tour actuel
        self.est_couche = False  # Indique si le joueur s'est couché
        self.all_in = False # Indique si le joueur est à tapis

    def recevoir_carte(self, carte):
        """Ajoute une carte à la main du joueur."""
        self.main.append(carte)

    def afficher_main(self):
        """Affiche la main du joueur."""
        print(f"Main de {self.nom}:")
        if self.main:
            for carte in self.main:
                print(carte)
        else:
            print("La main est vide.")

    def miser(self, montant):
        """
        Fait miser le joueur.

        Args:
            montant (int): Le montant à miser.

        Returns:
            bool: True si la mise est possible, False sinon (manque de jetons).
        """
        if 0 < montant <= self.jetons:
            self.jetons -= montant
            self.mise_courante += montant
            self.a_parle = True
            return True
        else:
            print(f"{self.nom} n'a pas assez de jetons pour miser {montant}.")
            return False

    def suivre(self, montant_a_suivre):
        """
        Fait suivre le joueur (miser le montant nécessaire pour égaler la mise).

        Args:
            montant_a_suivre (int): Le montant total à atteindre pour suivre.

        Returns:
            bool: True si le joueur a pu suivre, False sinon (manque de jetons).
        """
        montant_necessaire = montant_a_suivre - self.mise_courante
        if montant_necessaire <= 0:
            print(f"{self.nom} a déjà misé suffisamment.")
            self.a_parle = True
            return True
        elif montant_necessaire <= self.jetons:
            self.miser(montant_necessaire)
            return True
        else:
            print(f"{self.nom} n'a pas assez de jetons pour suivre.")
            return False

    def se_coucher(self):
        """Fait se coucher le joueur."""
        self.est_couche = True
        self.a_parle = True
        print(f"{self.nom} se couche.")

    def all_in(self):
        """Fait aller le joueur à tapis (miser tous ses jetons restants)."""
        montant_all_in = self.jetons
        if montant_all_in > 0:
            self.miser(montant_all_in)
            self.all_in = True
            print(f"{self.nom} fait tapis avec {montant_all_in} jetons.")
            return True
        else:
            print(f"{self.nom} n'a plus de jetons pour faire tapis.")
            return False

    def reinitialiser_pour_nouveau_tour(self):
        """Réinitialise l'état du joueur pour un nouveau tour."""
        self.main = []
        self.mise_courante = 0
        self.a_parle = False
        self.est_couche = False
        self.all_in = False

    def __str__(self):
        """Retourne une représentation lisible du joueur."""
        return f"Joueur {self.nom} ({self.jetons} jetons)"

    def __repr__(self):
        """Représentation de l'objet pour le débogage."""
        return f"Joueur(nom='{self.nom}', jetons={self.jetons})"