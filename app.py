import csv
import io
import json
import tempfile
import time
from pathlib import Path

import streamlit as st

from src import ingest
from src.continuity import comparer_plans
from src.dico import charger_dictionnaire, enrichir
from src.search import charger_memoire, chercher, format_temps, indexer, niveau

st.set_page_config(page_title="Lakta", page_icon="🎬", layout="wide")
ss = st.session_state
ss.setdefault("memoire", None)
ss.setdefault("dico", charger_dictionnaire())
ss.setdefault("q", "la scène où le père ouvre la fenêtre")

DEMO = {"video": "exemple (données fictives)", "chemin": None, "duree": None, "temps": None, "segments": [
    {"debut": 12.0, "fin": 27.5, "texte": "La mère parle de l’héritage pendant le dîner."},
    {"debut": 41.0, "fin": 58.0, "texte": "Le père ouvre la fenêtre et regarde la rue."},
    {"debut": 75.5, "fin": 90.0, "texte": "Aaslema, kifech el 7al ? Bienvenue dans la maison."},
    {"debut": 102.0, "fin": 118.0, "texte": "Ils préparent le couscous pour la fête de famille."}]}
try:
    DEMO["segments"] = charger_memoire("data/memoire_exemple.json")["segments"]
except FileNotFoundError:
    pass
OBJETS = ["vase", "cup", "bottle", "cell phone", "book", "clock", "chair", "person"]
vision, parole = ingest.disponibles()


@st.cache_resource(show_spinner="Chargement du modèle de recherche (premier lancement : plusieurs minutes)…")
def construire_index(cle, _segments, avec_dico, _dico):
    return indexer(_segments, _dico if avec_dico else None)


# ---------------------------------------------------------------- barre latérale
with st.sidebar:
    st.title("🎬 Lakta")
    st.caption("لقطة · la mémoire intelligente de vos rushes")
    source = st.radio("Source des rushes", ["Données d’exemple", "Ma vidéo"])
    if source == "Ma vidéo":
        if not (vision or parole):
            st.warning("Analyse de vidéo non installée. Lancez : pip install -r requirements-video.txt")
        else:
            fichier = st.file_uploader("Importer une courte vidéo (30 s à 3 min)", type=["mp4", "mov", "mkv", "webm"])
            if fichier and st.button("Analyser la vidéo", type="primary"):
                chemin = Path(tempfile.gettempdir()) / f"lakta_{fichier.name}"
                chemin.write_bytes(fichier.getbuffer())
                debut = time.perf_counter()
                segments, duree = [], None
                with st.spinner("Analyse en cours (en local, sans envoi de la vidéo)…"):
                    try:
                        duree = ingest.duree_video(chemin) if vision else None
                        segments = ingest.transcrire(chemin) if parole else []
                    except Exception as erreur:
                        st.error(f"L’analyse a échoué : {erreur}")
                ss.memoire = {"video": fichier.name, "chemin": str(chemin), "duree": duree,
                              "temps": time.perf_counter() - debut, "segments": segments}
    memoire = ss.memoire if (source == "Ma vidéo" and ss.memoire) else DEMO
    st.divider()
    st.caption(f"**Source active :** {memoire['video']}")
    if memoire["temps"]:
        st.metric("Temps de calcul", f"{memoire['temps']:.0f} s")
        if memoire["duree"]:
            st.caption(f"Vidéo de {memoire['duree']:.0f} s : un indicateur simple d’effort de calcul, pas une mesure d’énergie.")
    st.divider()
    st.markdown("**Nos engagements**\n- L’IA propose, le créateur décide\n- Chaque résultat montre sa source\n"
                "- Traitement local des rushes\n- Aucune modification automatique du montage")
    st.caption("Projet IA Éthique 360 · OIF × JEI INSAT")

st.title("🎬 Lakta")
st.caption("Retrouver, vérifier, créer : la mémoire intelligente de vos rushes.")
if memoire is DEMO:
    st.info("Mode démonstration : les résultats ci-dessous portent sur des données d’exemple fictives.")
t1, t2, t3, t4 = st.tabs(["🔎 Retrouver", "✅ Continuité", "🗣️ Mémoire culturelle", "⚖️ Éthique 360°"])

# ---------------------------------------------------------------- recherche
with t1:
    segments = memoire["segments"]
    st.write("Décrivez la scène ou la réplique recherchée, avec vos mots (français, arabe ou tunisien).")
    if memoire is DEMO:
        exemples = ["le père ouvre la fenêtre", "repas de famille", "salutation en tunisien"]
        for colonne, ex in zip(st.columns(len(exemples)), exemples):
            colonne.button(ex, use_container_width=True, on_click=lambda e=ex: ss.update(q=e))
    question = st.text_input("Votre recherche", key="q")
    c1, c2 = st.columns(2)
    k = c1.slider("Nombre de résultats", 1, 5, 3)
    avec_dico = c2.checkbox("Utiliser le dictionnaire tunisien", value=True)
    if not segments:
        st.warning("Aucune transcription disponible pour cette source (installez faster-whisper et relancez l’analyse).")
    elif question:
        try:
            vecteurs = construire_index(memoire["video"], segments, avec_dico, ss.dico)
            resultats = chercher(question, segments, vecteurs, k, ss.dico if avec_dico else None)
        except Exception as erreur:
            st.error(f"La recherche n’a pas pu démarrer : {erreur}")
            resultats = []
        if resultats and resultats[0]["termes"]:
            st.caption("Termes locaux reconnus : " + " · ".join(f"{t} → {s}" for t, s in resultats[0]["termes"]))
        for r in resultats:
            with st.container(border=True):
                g, d = st.columns([4, 1])
                g.subheader(f"De {format_temps(r['debut'])} à {format_temps(r['fin'])}")
                g.write(r["texte"])
                g.caption("Proposé par l’IA, à vérifier")
                d.metric("Similarité", f"{r['similarite']:.2f}", niveau(r["similarite"]), delta_color="off")
                if memoire["chemin"]:
                    try:
                        st.video(memoire["chemin"], start_time=int(r["debut"]), end_time=int(r["fin"]))
                    except TypeError:
                        st.video(memoire["chemin"], start_time=int(r["debut"]))
        st.caption("La similarité mesure la ressemblance de sens entre votre phrase et le passage. "
                   "Ce n’est pas une probabilité : les étiquettes forte, moyenne et faible sont indicatives.")

# ---------------------------------------------------------------- continuité
with t2:
    st.write("Comparez deux plans d’une même scène : l’outil signale les objets qui apparaissent ou disparaissent.")
    mode = st.radio("Mode", ["Saisie manuelle (démo)", "Depuis ma vidéo"], horizontal=True)
    plans = None
    if mode == "Saisie manuelle (démo)":
        a, b = st.columns(2)
        pa = a.multiselect("Objets au plan 3", OBJETS, default=["vase", "cup"])
        pb = b.multiselect("Objets au plan 5", OBJETS, default=["cup"])
        plans = ({"id": 3, "objets": set(pa)}, {"id": 5, "objets": set(pb)})
    elif not (memoire["chemin"] and vision and memoire["duree"]):
        st.warning("Importez et analysez une vidéo (menu de gauche) et installez requirements-video.txt.")
    else:
        duree = float(memoire["duree"])
        a, b = st.columns(2)
        sa = a.slider("Plan A (secondes)", 0.0, duree, 0.0, 0.5)
        sb = b.slider("Plan B (secondes)", 0.0, duree, min(duree, 5.0), 0.5)
        seuil = st.slider("Seuil de confiance de détection", 0.2, 0.8, 0.4, 0.05)
        if st.button("Comparer les deux plans", type="primary"):
            try:
                ia, ib = ingest.lire_image(memoire["chemin"], sa), ingest.lire_image(memoire["chemin"], sb)
                ss.cmp = {"A": (ia[:, :, ::-1], ingest.detecter_objets(ia, seuil)),
                          "B": (ib[:, :, ::-1], ingest.detecter_objets(ib, seuil))}
            except Exception as erreur:
                st.error(f"Comparaison impossible : {erreur}")
        if ss.get("cmp"):
            ci, cj = st.columns(2)
            ci.image(ss.cmp["A"][0], caption="Plan A : " + (", ".join(ss.cmp["A"][1]) or "aucun objet reconnu"))
            cj.image(ss.cmp["B"][0], caption="Plan B : " + (", ".join(ss.cmp["B"][1]) or "aucun objet reconnu"))
            plans = ({"id": "A", "objets": set(ss.cmp["A"][1])}, {"id": "B", "objets": set(ss.cmp["B"][1])})
    ignorer = set(st.multiselect("Objets à ignorer (ils bougent normalement)", OBJETS,
                                 default=["person"] if mode != "Saisie manuelle (démo)" else []))
    if plans:
        ecarts = comparer_plans(plans[0], plans[1], ignorer)
        lignes = []
        for i, e in enumerate(ecarts):
            with st.container(border=True):
                st.warning(e["texte"])
                choix = st.radio("Votre décision", ["À examiner", "Écart voulu", "À corriger"],
                                 key=f"dec_{mode}_{i}_{e['texte']}", horizontal=True)
                lignes.append((e["texte"], choix))
        if not ecarts:
            st.success("Aucune différence détectée entre les deux plans.")
        else:
            tampon = io.StringIO()
            ecrivain = csv.writer(tampon)
            ecrivain.writerow(["ecart", "decision"])
            ecrivain.writerows(lignes)
            st.download_button("Télécharger le rapport de continuité (CSV)", tampon.getvalue().encode("utf-8-sig"),
                               "rapport_continuite.csv", "text/csv")
            st.caption("Écart proposé par l’IA, décision prise par vous.")
    st.caption("Détection d’objets : modèle généraliste à 80 catégories. Les objets traditionnels ne sont pas reconnus, "
               "et des fausses alertes sont possibles (angle de caméra, objet caché).")

# ---------------------------------------------------------------- culture
with t3:
    st.write("Les outils d’IA comprennent mal le tunisien. Ce dictionnaire enrichit vos recherches avec l’équivalent français "
             "des termes locaux. **Liste de départ, à valider et compléter par des locuteurs.**")
    st.dataframe([{"terme": t, "sens": s} for t, s in sorted(ss.dico.items())], hide_index=True)
    phrase = st.text_input("Testez une phrase (lettres latines)", "Aaslema, kifech el 7al ? Barcha nass fil kahwa")
    enrichi, trouves = enrichir(phrase, ss.dico)
    st.write(enrichi)
    st.caption(f"{len(trouves)} terme(s) reconnu(s).")
    c1, c2, c3 = st.columns([2, 3, 1])
    nouveau = c1.text_input("Nouveau terme")
    sens = c2.text_input("Sens en français")
    if c3.button("Ajouter") and nouveau.strip() and sens.strip():
        ss.dico[nouveau.strip().lower()] = sens.strip()
        st.rerun()
    st.download_button("Télécharger le dictionnaire (JSON)", json.dumps(ss.dico, ensure_ascii=False, indent=2).encode("utf-8"),
                       "dictionnaire_tunisien.json", "application/json")

# ---------------------------------------------------------------- éthique
with t4:
    st.write("Les six angles de notre démarche, et ce que l’outil fait concrètement :")
    for titre, texte in [
        ("Créateurs", "L’outil signale, il ne modifie jamais le montage seul. Chaque écart attend votre décision."),
        ("Droits", "Les rushes restent au créateur et ne servent jamais à entraîner un modèle."),
        ("Données", "Tests sur des vidéos autorisées ; modèles ouverts dont les licences sont documentées dans le README."),
        ("Cultures et langues", "Dictionnaire tunisien enrichissable, limites du tunisien annoncées plutôt que cachées."),
        ("Transparence", "Chaque résultat montre sa source, son timecode et sa similarité, avec la mention « proposé par l’IA »."),
        ("Planète", "Modèles légers exécutés en local, analyse faite une seule fois, temps de calcul affiché."),
    ]:
        st.markdown(f"**{titre}.** {texte}")
    st.warning("Limites connues : la recherche sur des vidéos réelles en tunisien reste à mesurer ; la détection d’objets "
               "est généraliste ; la similarité n’est pas une probabilité.")