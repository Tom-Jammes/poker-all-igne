from models.cartes import Carte, Paquet

class TestCarte:
    def test_creation_carte(self):
        carte = Carte(10, "Coeur")
        assert carte.valeur == 10
        assert carte.couleur == "Coeur"

    def test_representation_str(self):
        carte_as_pique = Carte(1, "Pique")
        assert str(carte_as_pique) == "As de Pique"
        carte_roi_coeur = Carte(13, "Coeur")
        assert str(carte_roi_coeur) == "Roi de Coeur"
        carte_sept_trefle = Carte(7, "Trèfle")
        assert str(carte_sept_trefle) == "7 de Trèfle"

    def test_representation_repr(self):
        carte = Carte(11, "Carreau")
        assert repr(carte) == "Carte(valeur=11, couleur='Carreau')"

class TestPaquet:
    def test_creation_paquet(self):
        paquet = Paquet()
        assert len(paquet.cartes) == 52
        premiere_carte = paquet.cartes[0]
        assert isinstance(premiere_carte, Carte)
        assert premiere_carte.valeur == 1
        assert premiere_carte.couleur == "Coeur" # La première couleur générée

    def test_melanger_paquet(self):
        paquet1 = Paquet()
        paquet2 = Paquet()
        # Vérifier que les paquets sont identiques au départ
        assert [str(carte) for carte in paquet1.cartes] == [str(carte) for carte in paquet2.cartes]
        paquet2.melanger()
        # Il est très peu probable que les paquets restent identiques après le mélange
        assert [str(carte) for carte in paquet1.cartes] != [str(carte) for carte in paquet2.cartes]

    def test_tirer_carte(self):
        paquet = Paquet()
        nombre_cartes_initial = paquet.nombre_de_cartes()
        carte_tiree = paquet.tirer_carte()
        assert isinstance(carte_tiree, Carte)
        assert paquet.nombre_de_cartes() == nombre_cartes_initial - 1

    def test_tirer_carte_paquet_vide(self):
        paquet = Paquet()
        # Tirer toutes les cartes
        for _ in range(52):
            paquet.tirer_carte()
        # Tenter de tirer une carte d'un paquet vide
        carte_tiree = paquet.tirer_carte()
        assert carte_tiree is None

    def test_nombre_de_cartes(self):
        paquet = Paquet()
        assert paquet.nombre_de_cartes() == 52
        paquet.tirer_carte()
        assert paquet.nombre_de_cartes() == 51