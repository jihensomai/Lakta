"""Analyse d'une vidéo : transcription, images, objets visibles. Tout tourne en local.
Les bibliothèques lourdes sont importées à la demande : le reste du projet
fonctionne sans elles (voir requirements-video.txt)."""
import json
import time
from functools import lru_cache


def disponibles():
    """Renvoie (vision, parole) : les analyses possibles sur cet ordinateur."""
    def present(nom):
        try:
            __import__(nom)
            return True
        except ImportError:
            return False
    return present("cv2") and present("ultralytics"), present("faster_whisper")


def duree_video(chemin):
    import cv2
    v = cv2.VideoCapture(str(chemin))
    fps = v.get(cv2.CAP_PROP_FPS) or 25
    images = v.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    v.release()
    return images / fps


@lru_cache(maxsize=1)
def _whisper(modele):
    from faster_whisper import WhisperModel
    return WhisperModel(modele, device="cpu", compute_type="int8")


def transcrire(chemin_video, modele="small", langue=None):
    segments, _ = _whisper(modele).transcribe(str(chemin_video), language=langue)
    return [{"debut": round(s.start, 2), "fin": round(s.end, 2), "texte": s.text.strip()}
            for s in segments]


@lru_cache(maxsize=1)
def _yolo():
    from ultralytics import YOLO
    return YOLO("yolov8n.pt")


def lire_image(chemin_video, seconde):
    """Renvoie l'image (BGR) à la seconde demandée."""
    import cv2
    v = cv2.VideoCapture(str(chemin_video))
    v.set(cv2.CAP_PROP_POS_MSEC, seconde * 1000)
    ok, image = v.read()
    v.release()
    if not ok:
        raise ValueError(f"Impossible de lire l’image à {seconde:.1f} s")
    return image


def detecter_objets(image, seuil=0.4):
    """Objets reconnus (80 catégories généralistes COCO) avec une confiance >= seuil."""
    r = _yolo()(image, verbose=False)[0]
    return sorted({r.names[int(c)] for c, p in zip(r.boxes.cls, r.boxes.conf) if float(p) >= seuil})


def analyser(chemin_video, sortie="data/memoire.json", seuil=0.4):
    """Transcription + inventaire d'objets toutes les 2 secondes, enregistrés en JSON."""
    import cv2
    debut = time.perf_counter()
    memoire = {"video": str(chemin_video), "segments": transcrire(chemin_video), "objets": []}
    v = cv2.VideoCapture(str(chemin_video))
    fps = v.get(cv2.CAP_PROP_FPS) or 25
    total = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    v.release()
    for seconde in range(0, int(total / fps), 2):
        memoire["objets"].append({"temps": seconde, "objets": detecter_objets(lire_image(chemin_video, seconde), seuil)})
    memoire["secondes_de_calcul"] = round(time.perf_counter() - debut, 1)
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(memoire, f, ensure_ascii=False, indent=2)
    print(f"Mémoire enregistrée dans {sortie} ({memoire['secondes_de_calcul']} s)")


if __name__ == "__main__":
    import sys
    analyser(sys.argv[1])