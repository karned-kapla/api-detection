import pytest
from pydantic import ValidationError

from models.detection_model import DetectionWrite


def test_detection_creation():
    detection_data = {
        "name": "Detection Name",
        "description": "This is a detection description.",
        "price": 10.99,
        "quantity": 2,
        "number_of_persons": 4,
        "origin_country": "France",
        "attributes": ["vegan", "gluten-free"],
        "utensils": ["pan", "knife"],
        "ingredients": [
            {"name": "Sugar", "quantity": 100, "unit": "grams"},
            {"name": "Salt"}
        ],
        "steps": [
            {"step_number": 1, "description": "First step", "duration": "10 min"},
            {"step_number": 2, "description": "Second step"}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    detection = DetectionWrite(**detection_data)
    assert detection.name == "Detection Name"
    assert detection.description == "This is a detection description."
    assert detection.price == 10.99
    assert detection.quantity == 2
    assert detection.number_of_persons == 4
    assert detection.origin_country == "France"
    assert detection.attributes == ["vegan", "gluten-free"]
    assert detection.utensils == ["pan", "knife"]
    assert len(detection.ingredients) == 2
    assert len(detection.steps) == 2
    assert str(detection.thumbnail_url) == "http://example.com/thumbnail.jpg"
    assert str(detection.large_image_url) == "http://example.com/large_image.jpg"
    assert detection.source_reference == "Source Reference"


def test_detection_creation_with_defaults():
    detection_data = {
        "name": "Minimal Detection"
    }
    detection = DetectionWrite(**detection_data)
    assert detection.name == "Minimal Detection"
    assert detection.description is None
    assert detection.price is None
    assert detection.quantity is None
    assert detection.number_of_persons is None
    assert detection.origin_country is None
    assert detection.attributes == []
    assert detection.utensils == []
    assert detection.ingredients == []
    assert detection.steps == []
    assert detection.thumbnail_url is None
    assert detection.large_image_url is None
    assert detection.source_reference is None


def test_detection_validation_error():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "number_of_persons": 0
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)


def test_detection_missing_fields():
    incomplete_detection_data = {
        "description": "Incomplete Detection"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**incomplete_detection_data)

def test_detection_invalid_description_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "description": 123
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_price_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "price": "ten"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_quantity_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "quantity": "two"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_number_of_persons_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "number_of_persons": "four"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_origin_country_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "origin_country": 42
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_attributes_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "attributes": "vegan"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_utensils_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "utensils": "pan"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_ingredients_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "ingredients": "Sugar"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_steps_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "steps": "First step"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_thumbnail_url_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "thumbnail_url": 123
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_large_image_url_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "large_image_url": 123
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_source_reference_type():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "source_reference": 123
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_url():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "thumbnail_url": "invalid_url",
        "large_image_url": "invalid_url"
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)

def test_detection_invalid_list_types():
    invalid_detection_data = {
        "name": "Invalid Detection",
        "attributes": ["vegan", 123],
        "utensils": ["pan", 42]
    }
    with pytest.raises(ValidationError):
        DetectionWrite(**invalid_detection_data)