from fastapi import FastAPI, HTTPException, UploadFile
from src.models.input import FileInput, UriInput, UrlInput
from src.models.output import DetectionResult
from src.yolo_detection import prediction, uri_file_prediction, url_file_prediction
import base64

app = FastAPI(
    title="API Object Detection",
    version="1.0.0",
    description="Détection d'objets dans une image en utilisant un modèle YOLO (prédéfini ou personnalisé)",
)

@app.post("/file")
async def detect_objects_file(file: UploadFile) -> DetectionResult:
    image_bytes = await file.read()
    result = prediction(image_bytes, "yolo11l")
    return result

@app.post("/base64")
async def detect_objects(payload: FileInput) -> DetectionResult:
    try:
        image_bytes = base64.b64decode(payload.file_base64)
        return prediction(image_bytes, payload.model_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de décodage Base64 : {str(e)}")

@app.post("/uri")
async def detect_objects_uri(payload: UriInput) -> DetectionResult:
    return uri_file_prediction(payload.uri, payload.model_name)

@app.post("/url")
async def detect_objects_url(payload: UrlInput) -> DetectionResult:
    return url_file_prediction(str(payload.url), payload.model_name)