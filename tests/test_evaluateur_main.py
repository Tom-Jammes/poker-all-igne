from utils.evaluateur_main import EvaluateurDeMain
from models.cartes import Carte

class TestEvaluateurDeMain:

    @classmethod
    def setup_class(cls):
        """Méthode exécutée une seule fois avant tous les tests de cette classe."""
        # Mains pour les paires
        cls.mainPaire1 = [Carte(14, "C"), Carte(14, "D"), Carte(13, "C"), Carte(11, "T"), Carte(12, "P"), Carte(7, "C"), Carte(9, "T")]
        cls.mainPaire2 = [Carte(14, "C"), Carte(14, "D"), Carte(13, "C"), Carte(12, "T"), Carte(2, "P"), Carte(3, "C"), Carte(4, "T")]
        cls.mainPaire3 = [Carte(13, "C"), Carte(13, "D"), Carte(14, "C"), Carte(12, "T"), Carte(11, "P"), Carte(2, "C"), Carte(3, "T")]
        cls.mainPaire4 = [Carte(2, "C"), Carte(2, "D"), Carte(3, "C"), Carte(4, "T"), Carte(5, "P"), Carte(10, "C"), Carte(9, "T")]

        # Mains pour les doubles paires
        cls.mainDoublePaire1 = [Carte(14, "C"), Carte(14, "D"), Carte(13, "C"), Carte(13, "T"), Carte(12, "P"), Carte(11, "C"), Carte(9, "T")]
        cls.mainDoublePaire2 = [Carte(14, "C"), Carte(14, "D"), Carte(13, "C"), Carte(13, "T"), Carte(2, "P"), Carte(3, "C"), Carte(4, "T")]
        cls.mainDoublePaire3 = [Carte(14, "C"), Carte(14, "D"), Carte(12, "C"), Carte(12, "T"), Carte(13, "P"), Carte(2, "C"), Carte(3, "T")]
        cls.mainDoublePaire4 = [Carte(2, "C"), Carte(2, "D"), Carte(3, "C"), Carte(3, "T"), Carte(4, "P"), Carte(5, "C"), Carte(7, "T")]

        # Mains pour les brelans
        cls.mainBrelan1 = [Carte(14, "C"), Carte(14, "D"), Carte(14, "H"), Carte(13, "C"), Carte(12, "P"), Carte(11, "C"), Carte(9, "T")]
        cls.mainBrelan2 = [Carte(14, "C"), Carte(14, "D"), Carte(14, "H"), Carte(3, "C"), Carte(2, "P"), Carte(6, "C"), Carte(4, "T")]
        cls.mainBrelan3 = [Carte(13, "C"), Carte(13, "D"), Carte(13, "H"), Carte(14, "C"), Carte(12, "P"), Carte(11, "C"), Carte(2, "T")]
        cls.mainBrelan4 = [Carte(2, "C"), Carte(2, "D"), Carte(2, "H"), Carte(3, "C"), Carte(4, "P"), Carte(5, "C"), Carte(7, "T")]

        # Mains pour les quintes
        cls.mainQuinte1 = [Carte(14, "C"), Carte(13, "D"), Carte(12, "H"), Carte(11, "C"), Carte(10, "P"), Carte(2, "C"), Carte(3, "T")] # AKQJ10
        cls.mainQuinte2 = [Carte(9, "C"), Carte(10, "D"), Carte(11, "H"), Carte(12, "C"), Carte(13, "P"), Carte(2, "C"), Carte(3, "T")] # KQJT9
        cls.mainQuinte3 = [Carte(5, "C"), Carte(6, "D"), Carte(7, "H"), Carte(8, "C"), Carte(9, "P"), Carte(2, "C"), Carte(14, "T")] # 98765
        cls.mainQuinte4 = [Carte(14, "C"), Carte(2, "D"), Carte(3, "H"), Carte(4, "C"), Carte(5, "P"), Carte(10, "C"), Carte(5, "T")] # A2345

        # Mains pour les couleurs
        cls.mainCouleur1 = [Carte(14, "C"), Carte(13, "C"), Carte(12, "C"), Carte(11, "C"), Carte(9, "C"), Carte(8, "D"), Carte(7, "H")]
        cls.mainCouleur2 = [Carte(14, "S"), Carte(12, "S"), Carte(11, "S"), Carte(9, "S"), Carte(5, "S"), Carte(2, "D"), Carte(4, "H")]
        cls.mainCouleur3 = [Carte(13, "H"), Carte(12, "H"), Carte(11, "H"), Carte(9, "H"), Carte(5, "H"), Carte(2, "D"), Carte(4, "S")] # As bas
        cls.mainCouleur4 = [Carte(2, "D"), Carte(3, "D"), Carte(4, "D"), Carte(5, "D"), Carte(7, "D"), Carte(8, "C"), Carte(9, "S")]

        # Mains pour les full
        cls.mainFull1 = [Carte(14, "C"), Carte(14, "D"), Carte(14, "H"), Carte(13, "C"), Carte(13, "P"), Carte(12, "C"), Carte(11, "T")] # AAAKK
        cls.mainFull2 = [Carte(13, "C"), Carte(13, "D"), Carte(13, "H"), Carte(14, "C"), Carte(14, "P"), Carte(12, "C"), Carte(11, "T")] # TTTKK
        cls.mainFull3 = [Carte(2, "C"), Carte(2, "D"), Carte(2, "H"), Carte(14, "C"), Carte(14, "P"), Carte(12, "C"), Carte(1, "T")] # 333AA
        cls.mainFull4 = [Carte(2, "C"), Carte(2, "D"), Carte(2, "H"), Carte(3, "C"), Carte(3, "P"), Carte(4, "C"), Carte(5, "T")]   # 77722

        # Mains pour les carrés
        cls.mainCarre1 = [Carte(14, "C"), Carte(14, "D"), Carte(14, "H"), Carte(14, "S"), Carte(13, "C"), Carte(12, "C"), Carte(11, "T")] # AAAA K
        cls.mainCarre2 = [Carte(13, "C"), Carte(13, "D"), Carte(13, "H"), Carte(13, "S"), Carte(14, "P"), Carte(12, "C"), Carte(11, "T")] # TTTT 2
        cls.mainCarre3 = [Carte(3, "C"), Carte(3, "D"), Carte(3, "H"), Carte(3, "S"), Carte(14, "C"), Carte(13, "C"), Carte(12, "T")] # 3333 A
        cls.mainCarre4 = [Carte(2, "C"), Carte(2, "D"), Carte(2, "H"), Carte(2, "S"), Carte(3, "C"), Carte(4, "C"), Carte(5, "T")]   # 7777 5

        # Mains pour les quintes flush
        cls.mainQuinteFlush1 = [Carte(10, "C"), Carte(11, "C"), Carte(12, "C"), Carte(13, "C"), Carte(14, "C"), Carte(2, "D"), Carte(3, "H")] # AKQJT de coeur
        cls.mainQuinteFlush2 = [Carte(9, "S"), Carte(10, "S"), Carte(11, "S"), Carte(12, "S"), Carte(13, "S"), Carte(2, "D"), Carte(3, "H")] # KQJT9 de pique
        cls.mainQuinteFlush3 = [Carte(5, "H"), Carte(6, "H"), Carte(7, "H"), Carte(8, "H"), Carte(9, "H"), Carte(2, "D"), Carte(14, "C")] # 98765 de coeur
        cls.mainQuinteFlush4 = [Carte(14, "D"), Carte(2, "D"), Carte(3, "D"), Carte(4, "D"), Carte(5, "D"), Carte(10, "C"), Carte(9, "S")] # A2345 de carreau

        # Mains pour les quintes flush royales
        cls.mainQuinteFlushRoyale1 = [Carte(10, "C"), Carte(11, "C"), Carte(12, "C"), Carte(13, "C"), Carte(14, "C"), Carte(2, "D"), Carte(3, "H")] # AKQJT de coeur

        cls.evaluateur = EvaluateurDeMain()

    def test_evaluer_main_7_cartes_paires(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainPaire1) > self.evaluateur.evaluer_main_7_cartes(self.mainPaire2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainPaire2) > self.evaluateur.evaluer_main_7_cartes(self.mainPaire3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainPaire3) > self.evaluateur.evaluer_main_7_cartes(self.mainPaire4)

    def test_evaluer_main_7_cartes_double_paires(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire1) > self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire2) > self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire3) > self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire4)

    def test_evaluer_main_7_cartes_brelans(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainBrelan1) > self.evaluateur.evaluer_main_7_cartes(self.mainBrelan2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainBrelan2) > self.evaluateur.evaluer_main_7_cartes(self.mainBrelan3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainBrelan3) > self.evaluateur.evaluer_main_7_cartes(self.mainBrelan4)

    def test_evaluer_main_7_cartes_quintes(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinte1) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinte2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinte2) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinte3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinte3) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinte4)

    def test_evaluer_main_7_cartes_couleurs(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCouleur1) > self.evaluateur.evaluer_main_7_cartes(self.mainCouleur2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCouleur2) > self.evaluateur.evaluer_main_7_cartes(self.mainCouleur3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCouleur3) > self.evaluateur.evaluer_main_7_cartes(self.mainCouleur4)

    def test_evaluer_main_7_cartes_fulls(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainFull1) > self.evaluateur.evaluer_main_7_cartes(self.mainFull2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainFull2) > self.evaluateur.evaluer_main_7_cartes(self.mainFull3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainFull3) > self.evaluateur.evaluer_main_7_cartes(self.mainFull4)

    def test_evaluer_main_7_cartes_carres(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCarre1) > self.evaluateur.evaluer_main_7_cartes(self.mainCarre2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCarre2) > self.evaluateur.evaluer_main_7_cartes(self.mainCarre3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCarre3) > self.evaluateur.evaluer_main_7_cartes(self.mainCarre4)

    def test_evaluer_main_7_cartes_quinte_flush(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush1) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush2)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush2) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush3) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush4)

    def test_evaluer_main_7_cartes_mains_aleatoires(self):
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlushRoyale1) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush3)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinteFlush4) > self.evaluateur.evaluer_main_7_cartes(self.mainCarre1)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCarre4) > self.evaluateur.evaluer_main_7_cartes(self.mainFull1)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainFull4) > self.evaluateur.evaluer_main_7_cartes(self.mainCouleur1)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainCouleur4) > self.evaluateur.evaluer_main_7_cartes(self.mainQuinte1)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainQuinte4) > self.evaluateur.evaluer_main_7_cartes(self.mainBrelan1)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainBrelan4) > self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire1)
        assert self.evaluateur.evaluer_main_7_cartes(self.mainDoublePaire4) > self.evaluateur.evaluer_main_7_cartes(self.mainPaire1)