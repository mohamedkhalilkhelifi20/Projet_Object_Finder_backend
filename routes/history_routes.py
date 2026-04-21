from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from models.database import get_db, ScanHistory
from services.auth_service import verify_jwt_token
from schemas.schemas import SyncRequest, SyncResponse, HistoryResponse, HistoryItemResponse
from datetime import datetime

router = APIRouter(prefix="/history", tags=["History"])

# ─── GET /history
@router.get("", response_model=HistoryResponse)
def get_history(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        # 1. Vérifier le token JWT
        token   = authorization.replace("Bearer ", "")
        payload = verify_jwt_token(token)

        # 2. Récupérer l'historique de l'utilisateur
        history = db.query(ScanHistory).filter(
            ScanHistory.user_id == int(payload["sub"])).order_by(ScanHistory.detected_at.desc()).all()

        # 3. Formater la réponse
        return HistoryResponse(
            success = True,
            count   = len(history),
            history = [
                HistoryItemResponse(
                    id              = h.id,
                    label_fr        = h.label_fr,
                    distance_meters = h.distance_meters,
                    danger_level    = h.danger_level,
                    detected_at     = h.detected_at.isoformat(),
                )
                for h in history
            ]
        )

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
# ─── POST /history/sync
@router.post("/sync", response_model=SyncResponse)
def sync_history(
    request: SyncRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        # 1. Vérifier le token JWT
        token   = authorization.replace("Bearer ", "")
        payload = verify_jwt_token(token)
        user_id  = int(payload["sub"])

        # 2. Enregistrer les scans reçus en base
        saved_count = 0
        for item in request.detections:
            scan = ScanHistory(
                user_id         = user_id,
                label           = item.label,
                label_fr        = item.label_fr,
                distance_meters = item.distance_meters,
                danger_level    = item.danger_level,
                confidence      = item.confidence,
                voice_message   = item.voice_message,
                detected_at     = datetime.fromisoformat(item.detected_at),
            )
            db.add(scan)
            saved_count += 1

        db.commit()

        return SyncResponse(success=True, saved=saved_count)

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))