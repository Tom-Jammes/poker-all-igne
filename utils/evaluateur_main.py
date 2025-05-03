from itertools import combinations
from collections import Counter

class EvaluateurDeMain:
    VALEURS_STR_TO_INT = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def _get_valeur(self, carte):
        """Récupère la valeur numérique d'un objet Carte."""
        if isinstance(carte.valeur, str):
            return self.VALEURS_STR_TO_INT[carte.valeur.upper()]
        return carte.valeur

    def _est_quinte(self, valeurs_sortees):
        """Vérifie si une liste de valeurs triées constitue une quinte."""
        unique_valeurs = sorted(list(set(valeurs_sortees)), reverse=True)
        if len(unique_valeurs) < 5:
            return False, 0

        for i in range(len(unique_valeurs) - 4):
            if unique_valeurs[i] == unique_valeurs[i+1] + 1 == unique_valeurs[i+2] + 2 == unique_valeurs[i+3] + 3 == unique_valeurs[i+4] + 4:
                return True, unique_valeurs[i]

        if unique_valeurs[0] == 14 and ((unique_valeurs[3] == 5 and len(unique_valeurs) == 7)
                                        or (unique_valeurs[2] == 5 and len(unique_valeurs) == 6)
                                        or (unique_valeurs[1] == 5 and len(unique_valeurs) == 5)):
            return True, 5

        return False, 0

    def _evaluer_5_cartes(self, main_5_cartes):
        """Évalue une main de 5 objets Carte et retourne un score (méthode interne)."""
        if len(main_5_cartes) != 5:
            raise ValueError("Une main doit contenir 5 cartes.")

        valeurs = sorted([self._get_valeur(carte) for carte in main_5_cartes], reverse=True)
        couleurs = [carte.couleur for carte in main_5_cartes]
        counts = Counter(valeurs)
        couleur_flush = len(set(couleurs)) == 1

        if couleur_flush and valeurs == [14, 13, 12, 11, 10]:                       # Quinte flush royal (100 000)
            return 100000

        quinte, hauteur_quinte = self._est_quinte(valeurs)
        if couleur_flush and quinte:                                                # Quinte flush       (10 005 - 10 013)
            return 10000 + hauteur_quinte

        if 4 in counts.values():                                                    # Carré              (6203 - 7413)
            hauteur_carre = [v for v, count in counts.items() if count == 4][0]
            carte_restante = [v for v, count in counts.items() if count == 1][0]
            return 6000 + (hauteur_carre * 100) + carte_restante

        if 3 in counts.values() and 2 in counts.values():                           # Full               (4903 - 6113)
            hauteur_brelan = [v for v, count in counts.items() if count == 3][0]
            hauteur_paire = [v for v, count in counts.items() if count == 2][0]
            return 4700 + (hauteur_brelan * 100) + hauteur_paire

        if couleur_flush:                                                           # Couleur            (4621 - 4659)
            return 4600 + sum(valeurs)

        if quinte:                                                                  # Quinte             (4505 - 4514)
            return 4500 + hauteur_quinte

        if 3 in counts.values():                                                    # Brelan             (3223 - 4477)
            hauteur_brelan = [v for v, count in counts.items() if count == 3][0]
            cartes_restantes = sorted([v for v, count in counts.items() if count == 1], reverse=True)
            return 3000 + (hauteur_brelan * 100) + (cartes_restantes[0] * 5) + cartes_restantes[1]

        paires = [v for v, count in counts.items() if count == 2]
        if len(paires) == 2:                                                        # Double paire       (1744 - 3072)
            paire_haute = max(paires)
            paire_basse = min(paires)
            carte_restante = [v for v, count in counts.items() if count == 1][0]
            return 1400 + (paire_haute * 100) + (paire_basse * 20) + carte_restante

        if 2 in counts.values():                                                    # Paire              (429.3 - 1678.1)
            hauteur_paire = [v for v, count in counts.items() if count == 2][0]
            cartes_restantes = sorted([v for v, count in counts.items() if count == 1], reverse=True)
            return 200 + (hauteur_paire * 100) + (cartes_restantes[0] * 5) + (cartes_restantes[1]) + (cartes_restantes[2] * 0.1)

        return sum(valeurs)                                                         # Hauteur carte      (2 - 14)

    def evaluer_main_7_cartes(self, main_7_cartes):
        """Évalue la meilleure main de 5 cartes possible à partir de 7 objets Carte."""
        if len(main_7_cartes) != 7:
            raise ValueError("Une main de 7 cartes est requise.")

        meilleur_score = 0
        meilleure_combinaison = None
        for combinaison in combinations(main_7_cartes, 5):
            score = self._evaluer_5_cartes(list(combinaison))
            if score > meilleur_score:
                meilleur_score = score
                meilleure_combinaison = combinaison
        return meilleur_score, meilleure_combinaison