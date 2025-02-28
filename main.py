from fastapi import FastAPI, UploadFile
from src.yolo_detection import prediction, uri_file_prediction, url_file_prediction

app = FastAPI(
    title="API Object Detection",
    version="1.0.0",
    description="Détection d'objets dans une image en utilisant un modèle YOLO (prédéfini ou personnalisé)",
)


@app.post("/file")
async def detect_objects(file: UploadFile, model_name: str = "yolo11l"):
    image_bytes = await file.read()
    result = prediction(image_bytes, model_name)
    return result

@app.post("/uri")
async def detect_objects_uri(uri: str, model_name: str = "yolo11l"):
    result = uri_file_prediction(uri, model_name)
    return result

@app.post("/url")
async def detect_objects_url(url: str, model_name: str = "yolo11l"):
    result = url_file_prediction(url, model_name)
    return result