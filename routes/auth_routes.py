from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from services.auth_service import verify_google_token, get_or_create_user, create_jwt_token
from schemas.schemas import GoogleAuthRequest, GoogleAuthResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/google", response_model=GoogleAuthResponse)
def auth_google(request: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        # 1. Vérifier le token Google Firebase
        google_data = verify_google_token(request.id_token)

        # 2. Créer ou mettre à jour le user en base
        user = get_or_create_user(db, google_data)

        # 3. Générer un token JWT pour notre API
        jwt_token = create_jwt_token(user)

        # 4. Retourner le JWT + infos user
        return GoogleAuthResponse(
            access_token=jwt_token,
            email=user.email,
            name=user.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))