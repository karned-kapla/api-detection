import pytest
from typing import List, Dict, Any

from interfaces.detection_interface import DetectionRepository
from models.detection_model import DetectionWrite


class TestDetectionRepository(DetectionRepository):
    """
    A concrete implementation of the DetectionRepository interface for testing.
    """
    def __init__(self):
        self.detections = {}
        self.is_closed = False

    def create_detection(self, detection_create: DetectionWrite) -> str:
        detection_id = "test-uuid"
        self.detections[detection_id] = detection_create
        return detection_id

    def get_detection(self, detection_id: str) -> Dict[str, Any]:
        if detection_id in self.detections:
            return {"uuid": detection_id, "name": self.detections[detection_id].name}
        return None

    def list_detections(self) -> List[Dict[str, Any]]:
        return [{"uuid": detection_id, "name": detection.name} for detection_id, detection in self.detections.items()]

    def update_detection(self, detection_id: str, detection_update: DetectionWrite) -> None:
        if detection_id in self.detections:
            self.detections[detection_id] = detection_update

    def delete_detection(self, detection_id: str) -> None:
        if detection_id in self.detections:
            del self.detections[detection_id]

    def close(self) -> None:
        self.is_closed = True


def test_detection_repository_interface():
    """
    Test that a concrete implementation of DetectionRepository can be created
    and that it implements all the required methods.
    """
    # Create a concrete implementation
    repo = TestDetectionRepository()

    # Test create_detection
    detection = DetectionWrite(name="Test Detection")
    detection_id = repo.create_detection(detection)
    assert detection_id == "test-uuid"

    # Test get_detection
    retrieved_detection = repo.get_detection(detection_id)
    assert retrieved_detection["uuid"] == detection_id
    assert retrieved_detection["name"] == "Test Detection"

    # Test list_detections
    detections = repo.list_detections()
    assert len(detections) == 1
    assert detections[0]["uuid"] == detection_id
    assert detections[0]["name"] == "Test Detection"

    # Test update_detection
    updated_detection = DetectionWrite(name="Updated Detection")
    repo.update_detection(detection_id, updated_detection)
    retrieved_detection = repo.get_detection(detection_id)
    assert retrieved_detection["name"] == "Updated Detection"

    # Test delete_detection
    repo.delete_detection(detection_id)
    assert repo.get_detection(detection_id) is None

    # Test close
    repo.close()
    assert repo.is_closed


def test_detection_repository_abstract_methods():
    """
    Test that DetectionRepository cannot be instantiated directly
    because it has abstract methods.
    """
    with pytest.raises(TypeError) as exc:
        DetectionRepository()

    assert "Can't instantiate abstract class DetectionRepository" in str(exc.value)
    assert "abstract methods" in str(exc.value)