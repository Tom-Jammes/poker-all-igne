import random

class Carte:
    """Représente une carte à jouer."""
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def __str__(self):
        """Retourne une représentation lisible de la carte."""
        valeurs = {
            1: 'As', 11: 'Valet', 12: 'Dame', 13: 'Roi'
        }
        return f"{valeurs.get(self.valeur, str(self.valeur))} de {self.couleur}"

    def __repr__(self):
        """Représentation de l'objet pour le débogage."""
        return f"Carte(valeur={self.valeur}, couleur='{self.couleur}')"

class Paquet:
    """Représente un paquet de 52 cartes à jouer."""
    def __init__(self):
        self.cartes = self._creer_paquet()

    def _creer_paquet(self):
        """Crée un nouveau paquet de 52 cartes."""
        couleurs = ["Coeur", "Carreau", "Trèfle", "Pique"]
        valeurs = list(range(1, 14))  # De l'As (1) au Roi (13)
        return [Carte(valeur, couleur) for couleur in couleurs for valeur in valeurs]

    def melanger(self):
        """Mélange le paquet de cartes au hasard."""
        random.shuffle(self.cartes)

    def tirer_carte(self):
        """Tire la carte du dessus du paquet."""
        if self.cartes:
            return self.cartes.pop(0)
        else:
            return None  # Le paquet est vide

    def nombre_de_cartes(self):
        """Retourne le nombre de cartes restantes dans le paquet."""
        return len(self.cartes)