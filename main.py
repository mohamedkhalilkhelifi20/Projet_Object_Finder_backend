from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.firebase import init_firebase
from models.database import create_tables
from routes import auth_routes, detect_routes, history_routes

# 1. INITIALISER FIREBASE
init_firebase()


# 2. CRÉER L'APP FASTAPI
app = FastAPI(
    title="Object-Finder API",
    description="API de détection d'objets pour malvoyants — YOLOv8",
    version="1.0.0"
)

# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. CRÉER LES TABLES AU DÉMARRAGE
create_tables()

# 5.Routes
app.include_router(auth_routes.router)
app.include_router(detect_routes.router)
app.include_router(history_routes.router)

@app.get("/health")
def health():
    return {"status": "OK", "message": "API is running"}




    