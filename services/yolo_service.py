from ultralytics import YOLO
from services.detector import detect_objects
from services.distance import calculate_distance
from services.danger import get_danger_level, get_voice_message
from services.translator import translate
from datetime import datetime

model = YOLO("models/yolov8n.pt")

def analyze_image(image_bytes: bytes, lang: str = "fr") -> dict:
    try:
        # Étape 1 — Détection YOLOv8
        raw_detections, image_height = detect_objects(model, image_bytes)

        # Étape 2 — Calcul de la distance
        if not raw_detections:
            return {
                "success": True,
                "count":   0,
                "detections": [],
                "message": "Aucun objet détecté"
            }
        
        # Étape 3 — Enrichir chaque détection
        detections = []
        for det in raw_detections:
            label = det["label"]
            bbox_h = det["bbox_height"]
            conf = det["confidence"]

            # Calcul distance
            distance = calculate_distance(label, bbox_h,image_height)

            # Niveau de danger
            danger = get_danger_level(distance)

            # Traduction
            label_traduit = translate(label, lang=lang)

            # Message vocal
            message = get_voice_message(label_traduit, distance, danger, lang=lang)

            detections.append({
                "label":          label,
                "label_fr": label_traduit,
                "detected_at": datetime.now().isoformat(),
                "confidence":     conf,
                "distance_meters": distance,
                "danger_level":   danger,
                "voice_message":  message,
            })

        # Étape 4 — Trier par danger (DANGER en premier)
        ordre_danger = {"DANGER": 0, "ATTENTION": 1, "PROCHE": 2, "OK": 3}
        detections.sort(key=lambda x: ordre_danger[x["danger_level"]])

        return {
            "success":    True,
            "count":      len(detections),
            "detections": detections
        }

    except Exception as e:
        return {
            "success": False,
            "count":   0,
            "detections": [],
            "error":   str(e)
        }