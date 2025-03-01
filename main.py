from fastapi import FastAPI

from routers.v1 import router

app = FastAPI(
    title="API Object Detection", version="1.0.0",
    description="Détection d'objets dans une image en utilisant un modèle YOLO (prédéfini ou personnalisé)",
)

app.include_router(router)

