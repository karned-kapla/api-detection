import base64

from fastapi import FastAPI, HTTPException, UploadFile

from src.models.input import FileInput, ModelInput, UriInput, UrlInput
from src.models.output import ClassInfo, DetectionResult
from src.yolo_detection import get_model_classes, prediction, uri_file_prediction, url_file_prediction

app = FastAPI(
    title="API Object Detection", version="1.0.0",
    description="Détection d'objets dans une image en utilisant un modèle YOLO (prédéfini ou personnalisé)", )


@app.post("/file")
async def api_detect_objects_file( file: UploadFile ) -> DetectionResult:
    image_bytes = await file.read()
    result = prediction(image_bytes, "yolo11l")
    return result


@app.post("/base64")
async def api_detect_objects( payload: FileInput ) -> DetectionResult:
    try:
        image_bytes = base64.b64decode(payload.file_base64)
        return prediction(image_bytes, payload.model_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de décodage Base64 : {str(e)}")


@app.post("/uri")
async def api_detect_objects_uri( payload: UriInput ) -> DetectionResult:
    return uri_file_prediction(payload.uri, payload.model_name)


@app.post("/url")
async def api_detect_objects_url( payload: UrlInput ) -> DetectionResult:
    return url_file_prediction(str(payload.url), payload.model_name)


@app.get("/model/{model_name}/classes")
async def api_model_classes(model_name: str) -> list[ClassInfo]:
    return get_model_classes(model_name)