from fastapi import HTTPException
from common_api.middlewares.v1.database_middleware import check_repo
from common_api.utils.v0 import get_state_repos
from common_api.services.v0 import Logger
from config import KAFKA_TOPIC, MS_SECRET_TTL
from models.detection_model import DetectionCreate, DetectionCreateDatabase, DetectionRead, DetectionUpdate
from repositories import get_repositories
from services.cache_service import CacheService
from services.message_service import MessageService
from services.secret_service import SecretService

logger = Logger()

class DetectionService:
    def __init__(self):
        self.cache_service = CacheService()
        self.message_service = MessageService()
    
    def create_detection(self, request, detection: DetectionCreate) -> str:
        try:
            repos = get_state_repos(request)

            detection_db = DetectionCreateDatabase(**detection.model_dump())
            detection_db.status = "pending"
            detection_db.secret = SecretService.generate_secret()
            detection_db.created_by = request.state.token_info.get('user_uuid')

            detection_uuid = repos.detection_repo.create_detection(detection_db)
            
            if not isinstance(detection_uuid, str):
                raise TypeError("The method create_detection did not return a str.")

            credential = self.cache_service.get_database_credential(request.state.licence_uuid)

            payload = {
                "credential": credential,
                "licence_uuid": request.state.licence_uuid,
                "entity_uuid": request.state.entity_uuid
            }
            self.cache_service.store_context(detection_db.secret, payload, MS_SECRET_TTL)

            self.message_service.send_detection_task(
                topic=KAFKA_TOPIC,
                detection_uuid=detection_uuid,
                secret=detection_db.secret,
                url=detection_db.url,
                model=detection_db.model
            )
            
            return detection_uuid
        except Exception as e:
            logger.error(f"Error creating detection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the detection: {e}")
    
    def read_detection(self, request, uuid: str) -> DetectionRead:
        try:
            repos = get_state_repos(request)
            detection = repos.detection_repo.read_detection(uuid)
        except Exception as e:
            logger.error(f"Error reading detection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the detection: {e}")
        
        if detection is None:
            raise HTTPException(status_code=404, detail="Detection not found")
        
        return detection
    
    def update_detection(self, request, detection_update: DetectionUpdate) -> None:
        try:
            try:
                payload = self.cache_service.get_context(detection_update.secret)
                credential = payload["credential"]
            except ValueError as e:
                logger.error(f"Error getting context: {e}")
                raise HTTPException(status_code=403, detail="Invalid or expired secret")

            repos = get_repositories(uri=credential['uri'])
            check_repo(repos)

            setattr(request.state, 'licence_uuid', payload['licence_uuid'])
            setattr(request.state, 'entity_uuid', payload['entity_uuid'])
            setattr(request.state, 'repos', repos)

            existing_detection = repos.detection_repo.read_detection(detection_update.uuid)
            
            if not existing_detection:
                raise HTTPException(status_code=404, detail="Detection not found")

            if not SecretService.validate_secret(existing_detection.get('secret'), detection_update.secret):
                if existing_detection.get('secret') is None or existing_detection.get('secret') == "":
                    raise HTTPException(status_code=403, detail="Secret is required for update")
                else:
                    raise HTTPException(status_code=403, detail="Invalid secret")

            update_data = DetectionUpdate(
                uuid=detection_update.uuid,
                secret="",
                status="completed",
                model=detection_update.model,
                result=detection_update.result
            )

            repos.detection_repo.update_detection(detection_update.uuid, update_data)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating detection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the detection: {e}")
    
    def delete_detection(self, request, uuid: str) -> None:
        try:
            repos = get_state_repos(request)
            repos.detection_repo.delete_detection(uuid)
        except Exception as e:
            logger.error(f"Error deleting detection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the detection: {e}")