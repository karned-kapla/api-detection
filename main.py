import logging

from fastapi import FastAPI

from src.routers.v1 import router as router_v1
from src.routers.v2 import router as router_v2

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="API Object Detection",
    version="2.0.0",
    description="Détection d'objets dans une image en utilisant un modèle YOLO (prédéfini ou personnalisé)",
)

app.include_router(router_v1)
app.include_router(router_v2)

