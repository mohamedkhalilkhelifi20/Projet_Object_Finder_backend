from fastapi import APIRouter, File, UploadFile, Query
from services.yolo_service import analyze_image
from schemas.schemas import DetectResponse

router = APIRouter(prefix="/detect", tags=["Detection"])

@router.post("", response_model=DetectResponse)
async def detect(
    image: UploadFile = File(...),
    lang: str = Query(default="fr", enum=["fr", "tn"])
):
    image_bytes = await image.read()
    result      = analyze_image(image_bytes, lang=lang)
    return result