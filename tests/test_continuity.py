import unittest

from src.continuity import comparer_plans, verifier_continuite


class TestContinuite(unittest.TestCase):
    def test_objet_disparu_est_signale(self):
        plans = [{"id": 3, "objets": {"vase", "cup"}}, {"id": 5, "objets": {"cup"}}]
        self.assertEqual(verifier_continuite(plans),
                         ["« vase » présent au plan 3 mais absent du plan 5"])

    def test_plans_identiques_sans_alerte(self):
        plans = [{"id": 1, "objets": {"vase"}}, {"id": 2, "objets": {"vase"}}]
        self.assertEqual(verifier_continuite(plans), [])

    def test_objet_apparu_est_signale(self):
        ecarts = comparer_plans({"id": 1, "objets": set()}, {"id": 2, "objets": {"cup"}})
        self.assertEqual([e["type"] for e in ecarts], ["apparition"])

    def test_objet_ignore_n_est_pas_signale(self):
        plans = [{"id": 1, "objets": {"person", "vase"}}, {"id": 2, "objets": {"vase"}}]
        self.assertEqual(verifier_continuite(plans, ignorer={"person"}), [])


if __name__ == "__main__":
    unittest.main()