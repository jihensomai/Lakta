# 🎬 Lakta

**Retrouver, vérifier, créer : la mémoire intelligente de vos rushes.**

*Lakta* désigne en arabe un plan, une prise, l'instant que l'on saisit. C'est exactement ce que l'outil aide à retrouver.

Projet réalisé pour **IA Éthique 360** (5ᵉ édition), un hackathon organisé par la Junior Entreprise INSAT et l'Organisation internationale de la Francophonie (OIF), sur l'intégration de l'IA dans les industries audiovisuelles à vocation culturelle.

---

## En deux minutes

Lakta est un assistant d'intelligence artificielle pour les monteurs et les réalisateurs. Il fait deux choses :

- **Il retrouve une séquence.** Vous décrivez une scène avec vos mots, en français, en arabe ou en tunisien. Lakta vous indique où elle se trouve, avec le début et la fin.
- **Il signale les écarts de continuité.** Un vase est présent dans un plan et absent du suivant ? Lakta vous le montre avec les deux images côte à côte.

**Le créateur reste toujours aux commandes : l'IA propose, c'est lui qui décide.**


---

## Le problème

> Les monteurs et réalisateurs indépendants rencontrent des difficultés à retrouver une séquence précise dans des heures de rushes et à repérer les fautes de montage, quand ils travaillent sans assistant ni scripte, ce qui leur fait perdre du temps et laisse passer des erreurs.

*(Les « rushes » sont les vidéos brutes tournées avant le montage.)*

### Comment nous l'avons détecté

Avant de concevoir une solution, nous avons écouté les personnes concernées :

- **Des entretiens** avec un monteur et un réalisateur de cinéma. Nous leur avons demandé comment ils retrouvent une séquence, quelles tâches leur prennent le plus de temps, comment ils vérifient la continuité et quelles difficultés ils rencontrent avec le dialecte tunisien.
- **Un formulaire en ligne**, partagé par une créatrice de contenu .

Ce que nous avons appris :

- **40 %** des répondants perdent du temps à chercher dans leurs rushes.
- **30 %** des répondants citent d'abord ces erreurs passées inaperçues.



### Ce qui existe déjà


Notre différence : le tunisien, l'arabe et le français mélangés, des rushes traités en local pour rester confidentiels, et un outil pensé pour les petites structures.

---

## La solution

Lakta analyse vos vidéos **une seule fois** et en garde une « mémoire ». Cette mémoire sert ensuite à trois choses.

**1. Retrouver.** Vous écrivez « la scène où le père ouvre la fenêtre ». Lakta classe les passages selon leur **sens**, pas seulement selon les mots exacts, et vous donne le début, la fin et la vidéo.

**2. Vérifier.** Vous choisissez deux plans d'une même scène. Lakta compare les objets visibles et signale ceux qui apparaissent ou disparaissent. Pour chaque écart, vous décidez : *à examiner*, *écart voulu* ou *à corriger*. Vous pouvez ensuite exporter un rapport.

**3. Comprendre la langue locale.** Un dictionnaire de termes tunisiens (« aaslema » = bonjour, « kifech » = comment…) enrichit vos recherches. Les utilisateurs peuvent l'agrandir.

### Qui fait quoi ?

- **L'IA** transcrit la parole, détecte les objets, classe les passages par ressemblance de sens.
- **Vous** corrigez les transcriptions, choisissez les passages, décidez de chaque écart et validez le dictionnaire.

Lakta ne génère aucun texte et n'invente rien : il **retrouve** des passages qui existent déjà dans vos vidéos.

---

## Où en est le projet

Nous préférons être clairs sur ce qui marche et sur ce qui reste à faire.

**Fonctionne et est testé**
- La comparaison de continuité (objets qui apparaissent ou disparaissent), avec des tests automatiques.
- Le dictionnaire tunisien et l'enrichissement des recherches.

**Fonctionne (sur des données d'exemple)**
- L'interface avec ses quatre onglets, les décisions et l'export du rapport.
- La recherche par le sens, sur quelques phrases fictives.

**Code écrit, pas encore testé sur de vraies vidéos**
- La transcription (Whisper).
- La détection d'objets (YOLO).

**À faire**
- Mesurer la qualité de la transcription en tunisien.
- Reconnaître des objets du patrimoine tunisien.
- Faire valider le dictionnaire par des locuteurs.

> En mode « Données d'exemple », les résultats portent sur des données fictives. Seul le mode « Ma vidéo » analyse un vrai fichier.

---

## Installation

Il vous faut **Python 3.10 ou plus récent** et **Git**.

**1. Récupérer le projet**

```bash
git clone https://github.com/jihensomai/Lakta.git
cd Lakta
```

**2. Installer les dépendances de base**

```bash
pip install -r requirements.txt
```

**3. Lancer l'application**

```bash
streamlit run app.py
```

Sous Windows, si la commande n'est pas reconnue : `python -m streamlit run app.py`.

**À savoir :** au premier lancement de la recherche, un modèle d'IA de plusieurs centaines de Mo est téléchargé. Il faut une connexion internet cette fois-là. Ensuite, tout fonctionne en local.

### Pour analyser vos propres vidéos (facultatif)

Cette partie est lourde (plusieurs Go avec les modèles) :

```bash
pip install -r requirements-video.txt
```

---

## Utilisation

**1. Choisir la source** (menu de gauche)
- *Données d'exemple* pour découvrir l'outil.
- *Ma vidéo* pour importer un fichier court (30 secondes à 3 minutes), puis cliquer sur « Analyser ».

**2. Onglet « Retrouver »**
Décrivez la scène. Chaque résultat affiche son moment dans la vidéo, son texte et une **similarité** (voir [Limites](#limites)). Avec une vidéo importée, le lecteur démarre au bon moment.

**3. Onglet « Continuité »**
- Mode manuel : cochez les objets visibles dans deux plans.
- Mode vidéo : choisissez deux instants et lancez la comparaison.

Décidez de chaque écart, puis téléchargez le rapport en CSV. Les personnes sont ignorées par défaut en mode vidéo, car elles bougent normalement.

**4. Onglet « Mémoire culturelle »**
Testez une phrase en tunisien, ajoutez des termes au dictionnaire et téléchargez-le.

**5. Onglet « Éthique 360° »**
Les six angles de notre démarche et les limites connues.

En ligne de commande, vous pouvez aussi analyser une vidéo avec :

```bash
python src/ingest.py data/ma_video.mp4
```

### Lancer les tests

```bash
python -m unittest discover -s tests -t .
```

Les tests vérifient que :
- un objet qui disparaît est bien signalé,
- deux plans identiques ne déclenchent aucune fausse alerte,
- un objet qui apparaît est bien signalé,
- un objet marqué « à ignorer » n'est pas signalé,
- un terme tunisien est bien enrichi de son équivalent français.

Ils prouvent que la **logique** est correcte. Ils ne prouvent pas encore que la détection marche sur de vraies vidéos.

---

## Comment ça marche

```
Vidéo
  ├─► Transcription (faster-whisper) ───► texte avec moments
  └─► Images ─► Détection d'objets (YOLO) ─► objets par plan
                          │
                          ▼
              MÉMOIRE DES RUSHES
                │                │
   Dictionnaire tunisien    Comparaison de plans
                │                │
                ▼                ▼
   Recherche par le sens   Alertes de continuité
                └───────┬────────┘
                 Interface Streamlit
```

**Les outils utilisés**
- `faster-whisper` : transformer la parole en texte avec les moments.
- `sentence-transformers` (modèle `paraphrase-multilingual-MiniLM-L12-v2`) : comprendre le sens des phrases.
- `ultralytics` (YOLOv8 nano) et `opencv-python` : reconnaître les objets visibles.
- `streamlit` : l'interface web locale.

**Les fichiers du projet**
- `app.py` : l'interface.
- `src/ingest.py` : analyse des vidéos.
- `src/search.py` : recherche par le sens.
- `src/continuity.py` : comparaison de plans.
- `src/dico.py` : dictionnaire tunisien.
- `data/` : le dictionnaire et des données d'exemple fictives.
- `tests/` : les tests automatiques.

---

## Démarche éthique à 360°

Nous avons examiné le projet sous six angles.

### 👤 Les créateurs
Lakta signale, il ne modifie jamais le montage seul. Chaque écart attend la décision du créateur.

### ⚖️ Les droits
Les rushes restent la propriété de leurs créateurs. Ils sont traités en local et ne servent jamais à entraîner un modèle. Nous n'utilisons aucun film dont nous n'avons pas les droits.

### 🗂️ Les données
Nos tests utilisent des données fictives, nos propres vidéos ou des contenus du domaine public. Les modèles sont ouverts et leurs licences sont indiquées plus bas.

### 🗣️ Les cultures et les langues
Les outils d'IA comprennent mal le tunisien, surtout mélangé au français et à l'arabe. Nous le reconnaissons et nous agissons :
- un dictionnaire de termes locaux enrichit les recherches,
- il est conçu pour être validé et complété par des locuteurs,
- nous prévoyons de mesurer et de publier honnêtement la qualité réelle de la transcription.

Les futures étiquettes culturelles devront être validées par des personnes de la culture concernée, pour éviter les stéréotypes.

### 🔍 La transparence
Chaque résultat affiche sa source, son moment dans la vidéo et la mention « proposé par l'IA, à vérifier ». Nous affichons une **similarité** et non une « confiance » : c'est une ressemblance de sens, pas une probabilité. Aucune reconnaissance faciale n'est utilisée.

### 🌍 La planète
Nous utilisons des modèles ouverts et légers, exécutés en local, et nous analysons chaque vidéo une seule fois. L'interface affiche le temps de calcul. C'est un indicateur simple d'effort, **pas une mesure d'énergie** : une mesure rigoureuse reste à faire.

---

## Limites

Nous préférons les annoncer plutôt que les cacher.

- **Fausses alertes possibles** : angle de caméra, objet caché par un acteur, objet mal reconnu. L'utilisateur peut les ignorer, mais le risque existe.
- **Un écart peut être voulu.** Seul le créateur le sait.
- **Détection généraliste** : le modèle reconnaît 80 catégories d'objets courants. Les objets traditionnels (jebba, chéchia…) ne sont pas reconnus.
- **Tunisien** : notre dictionnaire est très petit et non validé, et la qualité de transcription n'est pas encore mesurée.
- **La similarité n'est pas une probabilité.** Les étiquettes « forte », « moyenne » et « faible » sont indicatives et leurs seuils sont arbitraires.
- **Petite échelle** : le projet a été testé sur de petits exemples. Son comportement sur des centaines d'heures de rushes reste à démontrer.

---

## Modèle économique

Ce sont des hypothèses, à confirmer avec les retours de notre enquête.

Trois offres :

- **Jeune créateur** : pour les étudiants et les premiers projets. Un projet à la fois, recherche par le sens, tarif étudiant.
- **Pro** : pour les monteurs freelances et les petites productions. Projets illimités, recherche, alertes de continuité et dictionnaire personnalisé.
- **Studio** : pour les studios et les structures d'archives. Plusieurs utilisateurs, serveur privé pour les rushes confidentiels, archives et patrimoine.


---

## Feuille de route

- [ ] Tester la transcription et la détection sur de vraies vidéos courtes
- [ ] Mesurer la qualité de transcription en tunisien et publier le résultat
- [ ] Faire valider et agrandir le dictionnaire avec des locuteurs
- [ ] Ajouter des tests de recherche et de détection sur vidéo
- [ ] Reconnaître des objets du patrimoine (avec un jeu d'images annoté)
- [ ] Étendre l'outil aux archives de radio et de télévision
- [ ] Mesurer la consommation d'énergie par heure de rushes

---

## Équipe

- Asfour Nour : chef de projet et business (https://github.com/nourasfournabeul-rgb)
- Somai Jihen : responsable technique et continuité (https://github.com/jihensomai)
- Nayet Yahia Hene : IA parole, recherche et langues (https://github.com/he-ne)
- Khadraoui Khalil : design, interface et média (https://github.com/khalil629)
- Khedher Mohamed Aziz : terrain, éthique et culture  (https://github.com/azizkhedher1)

---

## Licences et crédits

Le code de Lakta est publié sous licence **MIT** (voir le fichier `LICENSE`).

Licences des composants utilisés, d'après leurs auteurs (**à vérifier avant toute commercialisation**) :
- Streamlit, sentence-transformers, OpenCV : Apache-2.0
- faster-whisper et modèles Whisper : MIT
- Ultralytics YOLO : **AGPL-3.0**, une licence contraignante en cas de diffusion commerciale. Pour un produit commercial, il faudrait envisager un détecteur à licence plus permissive.

Projet réalisé dans le cadre du hackathon **IA Éthique 360**, initiative de la Représentation de l'OIF pour l'Afrique du Nord, en partenariat avec la Junior Entreprise INSAT.
