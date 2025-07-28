from models.detection_model import DetectionCreate, DetectionRead, DetectionUpdate
from services.detection_service import DetectionService

detection_service = DetectionService()

def service_create_detection(request, detection: DetectionCreate) -> str:
    return detection_service.create_detection(request, detection)

def service_read_detection(request, uuid: str) -> DetectionRead:
    return detection_service.read_detection(request, uuid)

def service_update_detection(request, detection_update: DetectionUpdate) -> None:
    detection_service.update_detection(request, detection_update)

def service_delete_detection(request, uuid: str) -> None:
    detection_service.delete_detection(request, uuid)
