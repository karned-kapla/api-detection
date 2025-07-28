from common_api.middlewares.v1.database_middleware import check_repo
from fastapi import HTTPException
from config import KAFKA_TOPIC, MS_SECRET_TTL
from models.detection_model import DetectionCreate, DetectionCreateDatabase, DetectionRead, DetectionUpdate
from common_api.utils.v0 import get_state_repos

from repositories import get_repositories
from utils.kafka_util import KafkaProducer
import secrets
import string
import json

from common_api.services.v0 import Logger, get_redis_api_db

logger = Logger()

def generate_secret(length=32):
    alphabet = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))



def service_create_detection(request, detection: DetectionCreate) -> str:
    try:
        repos = get_state_repos(request)
        detection = DetectionCreateDatabase(**detection.model_dump())
        detection.status = "pending"
        detection.secret = generate_secret()
        detection.created_by = request.state.token_info.get('user_uuid')
        detection_uuid = repos.detection_repo.create_detection(detection)

        if not isinstance(detection_uuid, str):
            raise TypeError("The method service_create_detection did not return a str.")

        r = get_redis_api_db()
        cache_key = f"{request.state.licence_uuid}_database"
        credential = r.get(cache_key)
        json_string = credential.replace("'", "\"")
        credential = json.loads(json_string)

        payload = {
            "credential": credential,
            "licence_uuid": request.state.licence_uuid,
            "entity_uuid": request.state.entity_uuid
        }

        cache_key = f"context_{detection.secret}"
        r.set(cache_key, json.dumps(payload), ex=MS_SECRET_TTL)

        producer = KafkaProducer()
        producer.send_message(
            topic=KAFKA_TOPIC,
            message={
                "uuid": detection_uuid,
                "secret": detection.secret,
                "url": str(detection.url),
                "model": detection.model,
                "response": {
                    "canal": "api",
                    "url": f"http://karned-api-detection:8000/detection/v1/tasks/results"
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the detection: {e}")

    return detection_uuid


def service_read_detection(request, uuid: str) -> DetectionRead:
    try:
        repos = get_state_repos(request)
        detection = repos.detection_repo.read_detection(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the detection: {e}")

    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")

    return detection

def service_update_detection(request, detection_update: DetectionUpdate) -> None:
    try:
        r = get_redis_api_db()
        cache_key = f"context_{detection_update.secret}"
        payload = json.loads(r.get(cache_key))
        credential = payload["credential"]
        repos = get_repositories(uri=credential['uri'])
        check_repo(repos)

        setattr(request.state, 'licence_uuid', payload['licence_uuid'])
        setattr(request.state, 'entity_uuid', payload['entity_uuid'])
        setattr(request.state, 'repos', repos)

        existing_detection = repos.detection_repo.read_detection(detection_update.uuid)

        if not existing_detection:
            raise HTTPException(status_code=404, detail="Detection not found")

        if existing_detection.get('secret') is None or existing_detection.get('secret') == "":
            raise HTTPException(status_code=403, detail="Secret is required for update")

        if existing_detection.get('secret') != detection_update.secret:
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
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the detection: {e}")

def service_delete_detection(request, uuid: str) -> None:
    try:
        repos = get_state_repos(request)
        repos.detection_repo.delete_detection(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the detection: {e}")
