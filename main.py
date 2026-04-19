from fastapi import FastAPI, File, UploadFile, Query
from yolo_service import analyze_image

app = FastAPI(
    title="Object-Finder API",
    description="API de détection d'objets pour malvoyants — YOLOv8",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "OK", "message": "API is running"}


@app.post("/detect")
async def detect(
    image: UploadFile = File(...),
    lang: str = Query(default="fr", enum=["fr", "tn"])
):
    # Lire les bytes de l'image
    image_bytes = await image.read()

    # Analyser via yolo_service
    result = analyze_image(image_bytes, lang=lang)

    return result