from fastapi import APIRouter, HTTPException, status, Request
from config.config import API_TAG_NAME
from common_api.decorators.v0.check_permission import check_permissions
from models.detection_model import DetectionCreate, DetectionRead, DetectionUpdate, DetectionCreateDatabase
from common_api.services.v0 import Logger
from services.detections_service import service_create_detection, service_read_detection, service_update_detection, service_delete_detection

logger = Logger()

VERSION = "v1"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/detection/{VERSION}"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@check_permissions(['create'])
async def router_create_detection(request: Request, detection: DetectionCreate) -> dict:
    logger.api("POST /detection/v1/")
    new_uuid = service_create_detection(request, detection)
    return {"uuid": new_uuid}


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=DetectionRead)
@check_permissions(['read', 'read_own'])
async def router_read_detection(request: Request, uuid: str):
    logger.api("GET /detection/v1/{uuid}")
    detection = service_read_detection(request, uuid)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['delete', 'delete_own'])
async def router_delete_detection(request: Request, uuid: str):
    logger.api("DELETE /detection/v1/{uuid}")
    service_delete_detection(request, uuid)


@router.put("/tasks/results", status_code=status.HTTP_204_NO_CONTENT)
async def router_update_detection(request: Request, detection_update: DetectionUpdate):
    logger.api("PUT /detection/v1/tasks/results")
    service_update_detection(request, detection_update)
