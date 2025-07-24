from abc import ABC, abstractmethod
from models.detection_model import DetectionCreate, DetectionUpdate

class DetectionRepository(ABC):

    @abstractmethod
    def create_detection(self, detection_create: DetectionCreate):
        pass

    @abstractmethod
    def read_detection(self, detection_id: str):
        pass

    @abstractmethod
    def update_detection(self, detection_id: str, detection_update: DetectionUpdate):
        pass

    @abstractmethod
    def delete_detection(self, detection_id: str):
        pass

    @abstractmethod
    def close(self):
        pass