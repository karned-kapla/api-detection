from fastapi import APIRouter, HTTPException, UploadFile
import base64

from src.functions.kafka import send_message
from src.models.input import FileInput, ModelInput, UriInput, UrlInput
from src.models.output import ClassInfo, DetectionResult
from src.yolo_detection import get_model_classes, prediction, uri_file_prediction, url_file_prediction


API_TAG_NAME = "object-detection"
VERSION = "v2"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/object-detection/{VERSION}"
)


@router.post("/uri")
async def api_detect_objects_uri( payload: UriInput ) -> DetectionResult:
    return uri_file_prediction(payload.uri, payload.model_name)


@router.post("/url")
async def api_detect_objects_url( payload: UrlInput ) -> None:
    send_message('object-detection', {'url': str(payload.url), 'model_name': payload.model_name})


@router.get("/model/{model_name}/classes")
async def api_model_classes(model_name: str) -> list[ClassInfo]:
    return get_model_classes(model_name)