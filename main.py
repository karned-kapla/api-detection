from fastapi import FastAPI

from routers.v1 import router as router_v1
from routers.v2 import router as router_v2

app = FastAPI(
    title="API Object Detection",
    version="2.0.0",
    description="Détection d'objets dans une image en utilisant un modèle YOLO (prédéfini ou personnalisé)",
)

app.include_router(router_v1)
app.include_router(router_v2)

