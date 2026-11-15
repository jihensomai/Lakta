import unittest

from src.dico import charger_dictionnaire, enrichir


class TestDictionnaire(unittest.TestCase):
    def test_terme_tunisien_enrichi(self):
        texte, trouves = enrichir("Aaslema, kifech el 7al ?", {"aaslema": "bonjour", "kifech": "comment"})
        self.assertIn("bonjour", texte)
        self.assertEqual([t for t, _ in trouves], ["aaslema", "kifech"])

    def test_texte_sans_terme_inchange(self):
        self.assertEqual(enrichir("Le père ouvre la fenêtre.", {"barcha": "beaucoup"}), ("Le père ouvre la fenêtre.", []))

    def test_dictionnaire_fourni_se_charge(self):
        self.assertIn("barcha", charger_dictionnaire())


if __name__ == "__main__":
    unittest.main()