from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from models.database import User
from core.config import SECRET_KEY, ALGORITHM, EXPIRE_DAYS
from firebase_admin import auth as firebase_auth

# 1. VÉRIFIER LE TOKEN GOOGLE FIREBASE
def verify_google_token(id_token: str) -> dict:
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return {
            "google_uid": decoded["uid"],
            "email":      decoded.get("email", ""),
            "name":       decoded.get("name", "Utilisateur"),
        }
    except Exception as e:
        raise ValueError(f"Token Google invalide : {e}")

# 2. CRÉER OU METTRE À JOUR LE USER EN BASE
def get_or_create_user(db: Session, google_data: dict) -> User:
    user = db.query(User).filter(
        User.google_uid == google_data["google_uid"]
    ).first()

    if user:
        # User existant → update last_login
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
    else:
        # Nouveau user → créer en base
        user = User(
            email=google_data["email"],
            name=google_data["name"],
            google_uid=google_data["google_uid"],
            created_at = datetime.now(timezone.utc),
            last_login = datetime.now(timezone.utc),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# 3. GÉNÉRER UN TOKEN JWT POUR NOTRE API
def create_jwt_token(user: User) -> str:
    payload = {
        "sub":   str(user.id),
        "email": user.email,
        "name":  user.name,
        "exp":   datetime.now(timezone.utc) + timedelta(days=EXPIRE_DAYS),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# 4. VÉRIFIER UN JWT
def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token JWT expiré")
    except jwt.JWTError as e:
        raise ValueError(f"Token JWT invalide : {e}")