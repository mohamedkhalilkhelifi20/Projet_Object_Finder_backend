from pydantic import BaseModel

# AUTH
# INPUT → Flutter envoie le token Google
class GoogleAuthRequest(BaseModel):
    id_token: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
            }
        }
    }

# OUTPUT → Backend retourne le JWT + infos user
class GoogleAuthResponse(BaseModel):
    access_token: str
    email:        str
    name:         str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiJ9...",
                "email":        "user@gmail.com",
                "name":         "Mohamed Ali"
            }
        }
    }


# DETECTION
class DetectionItem(BaseModel):
    label:           str
    label_fr:        str
    distance_meters: float
    danger_level:    str
    confidence:      float
    voice_message:   str
    detected_at:     str

    model_config = {
        "json_schema_extra": {
            "example": {
                "label":           "chair",
                "label_fr":        "chaise",
                "confidence":      0.95,
                "distance_meters": 0.4,
                "danger_level":    "DANGER",
                "voice_message":   "DANGER ! chaise très proche !"
            }
        }
    }

# OUTPUT → réponse complète /detect
class DetectResponse(BaseModel):
    success:    bool
    count:      int
    detections: list[DetectionItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "count":   1,
                "detections": [{
                    "label":           "chair",
                    "label_fr":        "chaise",
                    "confidence":      0.95,
                    "distance_meters": 0.4,
                    "danger_level":    "DANGER",
                    "voice_message":   "DANGER ! chaise très proche !"
                }]
            }
        }
    }

# HISTORY
# INPUT → une détection à synchroniser
class HistoryItem(BaseModel):
    label:           str
    label_fr:        str
    distance_meters: float
    danger_level:    str
    confidence:      float
    voice_message:   str
    detected_at:     str

    model_config = {
        "json_schema_extra": {
            "example": {
                "label":           "person",
                "label_fr":        "personne",
                "distance_meters": 1.2,
                "danger_level":    "PROCHE",
                "confidence":      0.87,
                "voice_message":   "personne détectée à 1.2 mètres",
                "detected_at":     "2024-01-15T10:30:00"
            }
        }
    }

# INPUT → Flutter envoie token + liste détections
class SyncRequest(BaseModel):
    token:      str
    detections: list[HistoryItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiJ9...",
                "detections": [{
                    "label":           "person",
                    "label_fr":        "personne",
                    "distance_meters": 1.2,
                    "danger_level":    "PROCHE",
                    "confidence":      0.87,
                    "voice_message":   "personne détectée à 1.2 mètres",
                    "detected_at":     "2024-01-15T10:30:00"
                }]
            }
        }
    }

# OUTPUT → une détection depuis la base
class HistoryItemResponse(BaseModel):
    id:              int
    label_fr:        str
    distance_meters: float
    danger_level:    str
    detected_at:     str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id":              1,
                "label_fr":        "chaise",
                "distance_meters": 0.4,
                "danger_level":    "DANGER",
                "detected_at":     "2024-01-15T10:30:00"
            }
        }
    }

# OUTPUT → réponse complète /history
class HistoryResponse(BaseModel):
    success: bool
    count:   int
    history: list[HistoryItemResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "count":   2,
                "history": [
                    {
                        "id":              1,
                        "label_fr":        "chaise",
                        "distance_meters": 0.4,
                        "danger_level":    "DANGER",
                        "detected_at":     "2024-01-15T10:30:00"
                    },
                    {
                        "id":              2,
                        "label_fr":        "personne",
                        "distance_meters": 1.2,
                        "danger_level":    "PROCHE",
                        "detected_at":     "2024-01-15T10:31:00"
                    }
                ]
            }
        }
    }

# OUTPUT → réponse sync
class SyncResponse(BaseModel):
    success: bool
    saved:   int

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "saved":   3
            }
        }
    }