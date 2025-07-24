import re
from urllib.parse import urlparse
from uuid import uuid4

from pymongo import MongoClient

from interfaces.detection_interface import DetectionRepository
from models.detection_model import DetectionCreateDatabase, DetectionUpdate
from schemas.detection_schema import detection_serial

def check_uri(uri):
    if not re.match(r"^mongodb://", uri):
        raise ValueError("Invalid URI: URI must start with 'mongodb://'")


def extract_database(uri: str) -> str:
    parsed_uri = urlparse(uri)
    db_name = parsed_uri.path.lstrip("/")

    if not db_name:
        raise ValueError("L'URI MongoDB ne contient pas de nom de base de données.")

    return db_name


class DetectionRepositoryMongo(DetectionRepository):

    def __init__(self, uri):
        check_uri(uri)
        database = extract_database(uri)

        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client[database]
        self.collection = "detections"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def create_detection(self, detection_create: DetectionCreateDatabase) -> str:
        detection_data = detection_create.model_dump()
        if "url" in detection_data and detection_data["url"] is not None:
            detection_data["url"] = str(detection_data["url"])
        detection_id = str(uuid4())
        detection_data["_id"] = detection_id
        try:
            new_uuid = self.db[self.collection].insert_one(detection_data)
            return new_uuid.inserted_id
        except Exception as e:
            raise ValueError(f"Failed to create detection in database: {str(e)}")

    def read_detection(self, uuid: str) -> dict:
        result = self.db[self.collection].find_one({"_id": uuid})
        if result is None:
            return {}
        detection = detection_serial(result)
        return detection

    def update_detection(self, uuid: str, detection_update: DetectionUpdate) -> None:
        update_fields = detection_update.model_dump()
        update_fields.pop('created_by', None)
        update_fields.pop('uuid', None)
        update_data = {"$set": update_fields}
        self.db[self.collection].find_one_and_update({"_id": uuid}, update_data)


    def delete_detection(self, uuid: str) -> None:
        self.db[self.collection].delete_one({"_id": uuid})

    def close(self):
        self.client.close()
