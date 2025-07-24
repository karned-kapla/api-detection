from fastapi import APIRouter

from src.models.input import UrlInput
from src.models.output import ClassInfo, SendResponse
from src.treat import treat_url
from src.yolo_detection import get_model_classes


API_TAG_NAME = "object-detection"
VERSION = "v2"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/object-detection/{VERSION}"
)


@router.post("/url")
async def api_detect_objects_url( payload: UrlInput ) -> SendResponse:
    return treat_url(payload)


@router.get("/model/{model_name}/classes")
async def api_model_classes(model_name: str) -> list[ClassInfo]:
    return get_model_classes(model_name)