"""Détection d'écarts de continuité entre deux plans d'une même scène.
L'outil signale, le créateur décide : rien n'est jamais corrigé automatiquement."""


def comparer_plans(avant, apres, ignorer=frozenset()):
    """avant / apres : {"id": 3, "objets": {"vase", "cup"}}.
    Renvoie une liste d'écarts (dictionnaires) : disparitions et apparitions."""
    ecarts = []
    for objet in sorted(set(avant["objets"]) - set(apres["objets"])):
        if objet not in ignorer:
            ecarts.append({
                "type": "disparition", "objet": objet,
                "texte": f"« {objet} » présent au plan {avant['id']} mais absent du plan {apres['id']}",
            })
    for objet in sorted(set(apres["objets"]) - set(avant["objets"])):
        if objet not in ignorer:
            ecarts.append({
                "type": "apparition", "objet": objet,
                "texte": f"« {objet} » absent du plan {avant['id']} mais présent au plan {apres['id']}",
            })
    return ecarts


def verifier_continuite(plans, ignorer=frozenset()):
    """Compare chaque plan au suivant. Renvoie la liste des textes d'alerte."""
    textes = []
    for i in range(1, len(plans)):
        textes += [e["texte"] for e in comparer_plans(plans[i - 1], plans[i], ignorer)]
    return textes


if __name__ == "__main__":
    demo = [{"id": 3, "objets": {"vase", "cup"}}, {"id": 5, "objets": {"cup"}}]
    for alerte in verifier_continuite(demo):
        print(alerte)