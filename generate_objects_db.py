# generate_objects_db.py
# Génère objects_db.json depuis OpenImages V7 YAML (601 classes)
# + YOLOv8 (80 classes COCO)
# python generate_objects_db.py

import json
import urllib.request
from ultralytics import YOLO

# ─────────────────────────────────────────
# Étape 1 — Lire les 601 classes depuis le YAML officiel
# ─────────────────────────────────────────
YAML_URL = "https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/open-images-v7.yaml"

def load_open_images_classes() -> dict:
    """
    Lit le YAML OpenImages V7 depuis Ultralytics GitHub.
    Retourne dict { "person": 381, "car": 90, ... }
    """
    print("Chargement OpenImages V7 YAML...")
    classes = {}
    with urllib.request.urlopen(YAML_URL) as response:
        lines = response.read().decode("utf-8").splitlines()
        in_names = False
        for line in lines:
            if "names:" in line:
                in_names = True
                continue
            if in_names:
                if line.strip() == "" or (line[0] != " " and ":" in line and "names" not in line):
                    break
                if ":" in line:
                    parts = line.strip().split(":", 1)
                    if len(parts) == 2:
                        idx   = int(parts[0].strip())
                        label = parts[1].strip().lower()
                        classes[label] = idx
    print(f"✅ {len(classes)} classes OpenImages V7 chargées")
    return classes


# ─────────────────────────────────────────
# Étape 2 — Hauteurs réelles (mètres)
# ─────────────────────────────────────────
HAUTEURS = {
    "person": 1.70, "man": 1.75, "woman": 1.65, "boy": 1.20,
    "girl": 1.15, "bicycle": 1.10, "car": 1.50, "motorcycle": 1.10,
    "airplane": 5.00, "bus": 3.00, "train": 3.50, "truck": 2.50,
    "boat": 1.50, "van": 1.80, "ambulance": 2.20, "taxi": 1.50,
    "traffic light": 0.60, "fire hydrant": 0.70, "stop sign": 0.75,
    "parking meter": 1.20, "bench": 0.80, "chair": 0.90,
    "couch": 0.85, "bed": 0.60, "table": 0.75, "desk": 0.75,
    "door": 2.00, "window": 1.20, "shelf": 1.80, "wardrobe": 1.90,
    "refrigerator": 1.80, "microwave oven": 0.30, "oven": 0.60,
    "sink": 0.20, "toaster": 0.20, "tv": 0.60, "television": 0.60,
    "laptop": 0.25, "computer keyboard": 0.04, "computer mouse": 0.04,
    "mobile phone": 0.15, "tablet computer": 0.25,
    "bottle": 0.25, "cup": 0.12, "bowl": 0.10, "fork": 0.18,
    "knife": 0.20, "spoon": 0.16, "banana": 0.15, "apple": 0.08,
    "orange": 0.08, "pizza": 0.05, "sandwich": 0.08, "cake": 0.15,
    "cat": 0.25, "dog": 0.50, "bird": 0.20, "horse": 1.60,
    "cattle": 1.40, "sheep": 0.70, "elephant": 3.00, "bear": 1.20,
    "lion": 1.00, "giraffe": 4.50, "zebra": 1.50, "tiger": 1.00,
    "backpack": 0.50, "umbrella": 1.00, "handbag": 0.35,
    "suitcase": 0.60, "hat": 0.15, "glasses": 0.05,
    "watch": 0.04, "tree": 5.00, "building": 15.00,
    "stairs": 1.50, "ladder": 2.50, "wheelchair": 1.00,
    "bicycle helmet": 0.25, "helmet": 0.25, "stool": 0.60,
    "lamp": 0.50, "clock": 0.30, "vase": 0.30,
    "scissors": 0.18, "teddy bear": 0.35, "hair dryer": 0.25,
    "toothbrush": 0.18, "book": 0.25, "flower": 0.40,
    "plant": 0.40, "houseplant": 0.40, "candle": 0.20,
    "mirror": 1.20, "pillow": 0.50, "towel": 0.80,
    "surfboard": 1.80, "skateboard": 0.15, "tennis racket": 0.60,
    "guitar": 1.00, "piano": 1.20, "drum": 0.50,
    "printer": 0.30, "dishwasher": 0.85, "washing machine": 0.90,
}

# ─────────────────────────────────────────
# Étape 3 — Traductions français
# ─────────────────────────────────────────
LABELS_FR = {
    "person": "personne", "man": "homme", "woman": "femme",
    "boy": "garçon", "girl": "fille", "bicycle": "vélo",
    "car": "voiture", "motorcycle": "moto", "airplane": "avion",
    "bus": "bus", "train": "train", "truck": "camion",
    "boat": "bateau", "van": "camionnette", "ambulance": "ambulance",
    "taxi": "taxi", "traffic light": "feu de circulation",
    "fire hydrant": "bouche d'incendie", "stop sign": "panneau stop",
    "parking meter": "parcmètre", "bench": "banc", "chair": "chaise",
    "couch": "canapé", "bed": "lit", "table": "table",
    "desk": "bureau", "door": "porte", "window": "fenêtre",
    "shelf": "étagère", "wardrobe": "armoire",
    "refrigerator": "réfrigérateur", "microwave oven": "micro-ondes",
    "oven": "four", "sink": "évier", "toaster": "grille-pain",
    "television": "télévision", "laptop": "ordinateur portable",
    "computer keyboard": "clavier", "computer mouse": "souris",
    "mobile phone": "téléphone", "tablet computer": "tablette",
    "bottle": "bouteille", "cup": "tasse", "bowl": "bol",
    "fork": "fourchette", "knife": "couteau", "spoon": "cuillère",
    "banana": "banane", "apple": "pomme", "orange": "orange",
    "pizza": "pizza", "sandwich": "sandwich", "cake": "gâteau",
    "bread": "pain", "cat": "chat", "dog": "chien", "bird": "oiseau",
    "horse": "cheval", "cattle": "vache", "sheep": "mouton",
    "elephant": "éléphant", "bear": "ours", "lion": "lion",
    "giraffe": "girafe", "zebra": "zèbre", "tiger": "tigre",
    "backpack": "sac à dos", "umbrella": "parapluie",
    "handbag": "sac à main", "suitcase": "valise", "hat": "chapeau",
    "glasses": "lunettes", "watch": "montre", "tree": "arbre",
    "building": "bâtiment", "stairs": "escaliers", "ladder": "échelle",
    "wheelchair": "fauteuil roulant", "bicycle helmet": "casque vélo",
    "helmet": "casque", "stool": "tabouret", "lamp": "lampe",
    "clock": "horloge", "vase": "vase", "scissors": "ciseaux",
    "teddy bear": "peluche", "hair dryer": "sèche-cheveux",
    "toothbrush": "brosse à dents", "book": "livre",
    "flower": "fleur", "houseplant": "plante", "candle": "bougie",
    "mirror": "miroir", "pillow": "oreiller", "towel": "serviette",
    "surfboard": "planche de surf", "skateboard": "skateboard",
    "tennis racket": "raquette de tennis", "guitar": "guitare",
    "piano": "piano", "printer": "imprimante",
    "dishwasher": "lave-vaisselle", "washing machine": "machine à laver",
    "accordion": "accordéon", "alarm clock": "réveil",
    "balloon": "ballon", "barrel": "tonneau", "belt": "ceinture",
    "billboard": "panneau publicitaire", "blender": "mixeur",
    "boot": "botte", "briefcase": "mallette", "broccoli": "brocoli",
    "calculator": "calculatrice", "camera": "caméra",
    "canoe": "canoë", "carrot": "carotte", "castle": "château",
    "ceiling fan": "ventilateur de plafond", "cheese": "fromage",
    "christmas tree": "sapin de noël", "coat": "manteau",
    "croissant": "croissant", "cucumber": "concombre",
    "curtain": "rideau", "deer": "cerf", "dishwasher": "lave-vaisselle",
    "doll": "poupée", "donut": "donut", "dress": "robe",
    "drum": "tambour", "duck": "canard", "eagle": "aigle",
    "egg (food)": "œuf", "envelope": "enveloppe", "flag": "drapeau",
    "flashlight": "lampe de poche", "frying pan": "poêle",
    "goldfish": "poisson rouge", "grape": "raisin",
    "guitar": "guitare", "hamburger": "hamburger", "hammer": "marteau",
    "headphones": "casque audio", "helicopter": "hélicoptère",
    "high heels": "talons hauts", "hot dog": "hot-dog",
    "ice cream": "glace", "jacket": "veste", "jeans": "jeans",
    "kettle": "bouilloire", "kite": "cerf-volant", "koala": "koala",
    "ladder": "échelle", "lamp": "lampe", "lemon": "citron",
    "leopard": "léopard", "lipstick": "rouge à lèvres",
    "lobster": "homard", "microphone": "microphone",
    "monkey": "singe", "muffin": "muffin", "mug": "mug",
    "mushroom": "champignon", "necklace": "collier",
    "ostrich": "autruche", "panda": "panda", "parachute": "parachute",
    "parrot": "perroquet", "pasta": "pâtes", "peach": "pêche",
    "pear": "poire", "pen": "stylo", "penguin": "pingouin",
    "pig": "cochon", "pineapple": "ananas", "plate": "assiette",
    "polar bear": "ours polaire", "popcorn": "popcorn",
    "potato": "pomme de terre", "pumpkin": "citrouille",
    "rabbit": "lapin", "raccoon": "raton laveur",
    "rose": "rose", "salad": "salade", "saxophone": "saxophone",
    "scarf": "écharpe", "scoreboard": "tableau de score",
    "screwdriver": "tournevis", "shark": "requin",
    "shirt": "chemise", "shorts": "short", "shower": "douche",
    "ski": "ski", "skirt": "jupe", "skyscraper": "gratte-ciel",
    "snake": "serpent", "snowboard": "snowboard", "snowman": "bonhomme de neige",
    "sock": "chaussette", "spider": "araignée", "squirrel": "écureuil",
    "stapler": "agrafeuse", "strawberry": "fraise",
    "street light": "lampadaire", "suit": "costume",
    "swan": "cygne", "swimming pool": "piscine", "sword": "épée",
    "taco": "taco", "tank": "char", "teapot": "théière",
    "telephone": "téléphone", "tent": "tente", "tie": "cravate",
    "tiger": "tigre", "tire": "pneu", "toilet": "toilettes",
    "tomato": "tomate", "torch": "torche", "tortoise": "tortue",
    "treadmill": "tapis roulant", "trophy": "trophée",
    "trumpet": "trompette", "turtle": "tortue marine",
    "violin": "violon", "waffle": "gaufre",
    "watermelon": "pastèque", "whale": "baleine",
    "wheelchair": "fauteuil roulant", "wine glass": "verre à vin",
    "wrench": "clé anglaise", "zebra": "zèbre",
    "zucchini": "courgette",
}

# ─────────────────────────────────────────
# Étape 4 — Traductions tunisiennes
# ─────────────────────────────────────────
LABELS_TN = {
    "person": "واحد", "man": "راجل", "woman": "مرا",
    "boy": "ولد", "girl": "بنت", "bicycle": "بيسكليت",
    "car": "كرهبة", "motorcycle": "موتو", "airplane": "طيارة",
    "bus": "كار", "train": "تران", "truck": "كاميون",
    "boat": "قارب", "van": "فان", "ambulance": "سيارة إسعاف",
    "taxi": "تاكسي", "traffic light": "فنار",
    "fire hydrant": "بوبينة", "stop sign": "بلاكا ستوب",
    "bench": "بنكيت", "chair": "كرسي", "couch": "كنابي",
    "bed": "سرير", "table": "طاولة", "desk": "بيرو",
    "door": "باب", "window": "شباك", "shelf": "رف",
    "wardrobe": "أرموار", "refrigerator": "فريدجيدار",
    "microwave oven": "ميكرو", "oven": "كوزينة",
    "sink": "حوض", "toaster": "توستور", "television": "تيلي",
    "laptop": "لابتوب", "computer keyboard": "كيبورد",
    "computer mouse": "سوريس", "mobile phone": "تيليفون",
    "bottle": "قرعة", "cup": "كاسة", "bowl": "طاسة",
    "fork": "فرشيطة", "knife": "موس", "spoon": "معلقة",
    "banana": "بنان", "apple": "تفاحة", "orange": "ليمون",
    "pizza": "بيتزا", "sandwich": "كاسكروت", "cake": "كاتو",
    "bread": "خبز", "cat": "قطوس", "dog": "كلب",
    "bird": "طير", "horse": "عود", "cattle": "بقرة",
    "sheep": "خروف", "elephant": "فيل", "bear": "دب",
    "lion": "سبع", "giraffe": "زرافة", "zebra": "زيبرا",
    "tiger": "نمر", "backpack": "شنطة الضهر",
    "umbrella": "مظلة", "handbag": "شنطة", "suitcase": "ڤاليز",
    "hat": "شاشية", "glasses": "نضارة", "watch": "ساعة",
    "tree": "شجرة", "building": "عمارة", "stairs": "دراج",
    "wheelchair": "كرسي معاق", "helmet": "خوذة",
    "stool": "كرسي صغير", "lamp": "لمبة", "clock": "ساعة حيط",
    "vase": "فاز", "scissors": "مقص", "teddy bear": "دمية",
    "toothbrush": "فرشة سنان", "book": "كتاب",
    "flower": "وردة", "candle": "شمعة", "mirror": "مراية",
    "pillow": "مخدة", "towel": "فوطة", "guitar": "قيتارة",
    "drum": "طبلة", "balloon": "بالونة", "camera": "كاميرا",
    "belt": "سانطور", "coat": "كابوط", "dress": "روبة",
    "duck": "بطة", "egg (food)": "بيضة", "flag": "علم",
    "hamburger": "هامبرغر", "hat": "شاشية",
    "ice cream": "آيس كريم", "jacket": "جاكيت",
    "jeans": "جينز", "kettle": "برادة", "lemon": "حامض",
    "microphone": "ميكرو", "monkey": "قرد", "mug": "ماق",
    "mushroom": "فقع", "necklace": "قلادة", "panda": "باندا",
    "parrot": "ببغاء", "pasta": "معكرونة", "pen": "قلم",
    "pig": "خنزير", "pineapple": "أناناس", "plate": "طبسي",
    "popcorn": "فشار", "potato": "بطاطا", "rabbit": "قنية",
    "rose": "وردة", "salad": "سلاطة", "scarf": "إيشارب",
    "shirt": "قميص", "shorts": "شورت", "shower": "دوش",
    "ski": "سكي", "snake": "حنش", "sock": "شرّاب",
    "spider": "عنكبوت", "strawberry": "فريز",
    "suit": "كوستيم", "swan": "بجعة", "sword": "سيف",
    "teapot": "برّاد", "telephone": "تيليفون", "tent": "خيمة",
    "tie": "كرافاط", "tire": "كاوتش", "toilet": "بيت الما",
    "tomato": "طماطم", "tortoise": "فقرون",
    "trumpet": "ترومبيت", "violin": "كمان",
    "waffle": "غوفر", "watermelon": "دلاع",
    "whale": "حوت", "wine glass": "كاس",
    "wrench": "كلاو فرنسي", "zucchini": "قرعة",
}


# ─────────────────────────────────────────
# Étape 5 — Génération finale
# ─────────────────────────────────────────
def generate():
    # Charger YOLOv8 (80 classes COCO)
    print("Chargement YOLOv8...")
    model = YOLO("models/yolov8n.pt")
    yolo_classes = {v.lower(): k for k, v in model.names.items()}
    print(f"✅ {len(yolo_classes)} classes YOLOv8 chargées")

    # Charger OpenImages V7 (601 classes)
    oi_classes = load_open_images_classes()

    # Fusionner toutes les sources
    all_labels = set()
    all_labels.update(yolo_classes.keys())
    all_labels.update(oi_classes.keys())
    all_labels.update(HAUTEURS.keys())

    print(f"\n📦 Total classes fusionnées : {len(all_labels)}")

    objects_db = {}
    missing_fr = []
    missing_tn = []
    missing_hauteur = []

    for label in sorted(all_labels):
        fr      = LABELS_FR.get(label)
        tn      = LABELS_TN.get(label)
        hauteur = HAUTEURS.get(label, 0.50)
        in_yolo = label in yolo_classes
        in_oi   = label in oi_classes

        if not fr:
            missing_fr.append(label)
            fr = label
        if not tn:
            missing_tn.append(label)
            tn = label

        objects_db[label] = {
            "hauteur":  hauteur,
            "fr":       fr,
            "tn":       tn,
            "in_yolo":  in_yolo,
            "in_oi":    in_oi,
        }

    # Sauvegarder
    with open("objects_db.json", "w", encoding="utf-8") as f:
        json.dump(objects_db, f, ensure_ascii=False, indent=2)

    # Rapport
    print("\n" + "="*50)
    print("✅ objects_db.json généré !")
    print(f"   Total objets           : {len(objects_db)}")
    print(f"   Détectables YOLOv8     : {sum(1 for v in objects_db.values() if v['in_yolo'])}")
    print(f"   Dans OpenImages V7     : {sum(1 for v in objects_db.values() if v['in_oi'])}")
    print(f"   FR manquantes          : {len(missing_fr)}")
    print(f"   TN manquantes          : {len(missing_tn)}")
    print(f"   Hauteurs par défaut    : {len(missing_hauteur)}")
    print("="*50)


if __name__ == "__main__":
    generate()