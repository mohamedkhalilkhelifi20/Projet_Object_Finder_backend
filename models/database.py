from sqlalchemy import (
    create_engine, Column, Integer, String, 
    Float, DateTime, ForeignKey
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# 1. CONNEXION BASE DE DONNÉES
DATABASE_URL = "sqlite:///./object_finder.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. TABLE USERS

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    name       = Column(String, nullable=False)
    google_uid = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relation → un user a plusieurs détections
    detections = relationship("ScanHistory", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

# 3. TABLE SCAN_HISTORY
class ScanHistory(Base):
    __tablename__ = "scan_history"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    label           = Column(String, nullable=False)   # "chair"
    label_fr        = Column(String, nullable=False)   # "chaise"
    distance_meters = Column(Float, nullable=False)    # 0.4
    danger_level    = Column(String, nullable=False)   # "DANGER"
    confidence      = Column(Float, nullable=False)    # 0.95
    voice_message   = Column(String, nullable=False)   # "DANGER ! chaise très proche !"
    detected_at     = Column(DateTime, default=datetime.utcnow)

    # Relation → appartient à un user
    user = relationship("User", back_populates="detections")

    def __repr__(self):
        return f"<ScanHistory {self.label_fr} {self.distance_meters}m>"

# 4. CRÉER LES TABLES
def create_tables():
    Base.metadata.create_all(bind=engine)

# 5. DEPENDENCY INJECTION pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
