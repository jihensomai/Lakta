"""Recherche sémantique dans la transcription des rushes : le sens compte,
pas seulement les mots exacts. L'IA retrouve, elle ne génère aucun texte."""
import json

import numpy as np

from src.dico import enrichir

MODELE = "paraphrase-multilingual-MiniLM-L12-v2"
_encodeur = None


def encodeur():
    global _encodeur
    if _encodeur is None:
        from sentence_transformers import SentenceTransformer  # import à la demande
        _encodeur = SentenceTransformer(MODELE)
    return _encodeur


def charger_memoire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def indexer(segments, dico=None):
    textes = [enrichir(s["texte"], dico)[0] if dico else s["texte"] for s in segments]
    return encodeur().encode(textes, normalize_embeddings=True)


def chercher(question, segments, vecteurs, k=3, dico=None):
    texte, termes = enrichir(question, dico) if dico else (question, [])
    q = encodeur().encode([texte], normalize_embeddings=True)[0]
    scores = vecteurs @ q
    ordre = np.argsort(-scores)[:k]
    return [{**segments[i], "similarite": float(scores[i]), "termes": termes} for i in ordre]


def niveau(similarite):
    """Étiquette indicative (seuils arbitraires, à calibrer) : ce n'est PAS une probabilité."""
    return "forte" if similarite >= 0.55 else "moyenne" if similarite >= 0.35 else "faible"


def format_temps(secondes):
    s = int(secondes)
    return f"{s // 60:02d}:{s % 60:02d}"