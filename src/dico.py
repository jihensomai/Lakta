"""Couche culturelle : un petit dictionnaire de termes du dialecte tunisien
(écrits en lettres latines) avec leur équivalent français.

Avant la recherche sémantique, les textes et les requêtes sont enrichis de ces
équivalents, car les modèles multilingues comprennent mal le tunisien.
La liste de départ est à faire valider et compléter par des locuteurs."""
import json
import re
from pathlib import Path

CHEMIN = Path(__file__).resolve().parent.parent / "data" / "dictionnaire_tunisien.json"
MOT = re.compile(r"[\w']+", re.UNICODE)


def charger_dictionnaire(chemin=CHEMIN):
    try:
        with open(chemin, encoding="utf-8") as f:
            return {k.lower(): v for k, v in json.load(f).items()}
    except FileNotFoundError:
        return {}


def enrichir(texte, dico):
    """Ajoute l'équivalent français après chaque terme connu.
    Renvoie (texte enrichi, liste de (terme, sens) reconnus)."""
    trouves = []
    for mot in MOT.findall(texte.lower()):
        if mot in dico and mot not in [t for t, _ in trouves]:
            trouves.append((mot, dico[mot]))
    if not trouves:
        return texte, []
    ajout = " ".join(f"({m} : {fr})" for m, fr in trouves)
    return f"{texte} {ajout}", trouves