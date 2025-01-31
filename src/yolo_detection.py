import requests
from fastapi import HTTPException
from google.cloud import storage
from ultralytics import YOLO
import cv2
import numpy as np

def load_model(model_name: str) -> YOLO:
    model = YOLO(f"models/{model_name}.pt")
    return model

def add_shape(image: np.ndarray, datas: dict) -> dict:
    datas["shape"] = image.shape
    return datas

def add_speed(results: list, datas: dict) -> dict:
    datas["speed"] = results[0].speed
    return datas

def add_detections(model: YOLO, results: list, datas: dict) -> dict:
    detections = []
    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.5:
                detections.append(
                    {
                        "xmin": float(box.xyxy[0][0]),
                        "ymin": float(box.xyxy[0][1]),
                        "xmax": float(box.xyxy[0][2]),
                        "ymax": float(box.xyxy[0][3]),
                        "confidence": float(box.conf[0]),
                        "predicted_class": int(box.cls[0]),
                        "name": model.names[int(box.cls[0])]
                    }
                )
    datas["boxes"] = detections
    return datas

def construct_datas(model: YOLO, results: list, image: np.ndarray) -> dict:
    datas = {}
    datas = add_shape(image=image, datas=datas)
    datas = add_speed(results=results, datas=datas)
    datas = add_detections(model=model, results=results, datas=datas)
    return datas

def treat_image(image_bytes: bytes) -> np.ndarray:
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def download_image_from_gcs(gcs_uri: str) -> bytes:
    try:
        if gcs_uri.startswith("gs://"):
            gcs_uri = gcs_uri[5:]
        bucket_name, blob_path = gcs_uri.split('/', 1)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        image_bytes = blob.download_as_bytes()
        return image_bytes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'image : {str(e)}")


def prediction(image_bytes: bytes, model_name: str) -> dict:
    image = treat_image(image_bytes)
    model = load_model(model_name)
    results = model.predict(image)
    datas = construct_datas(model=model, results=results, image=image)
    return datas

def uri_file_prediction(uri: str, model_name: str) -> dict:
    image_bytes = download_image_from_gcs(uri)
    return prediction(image_bytes, model_name)

def url_file_prediction(url: str, model_name: str) -> dict:
    image_bytes = requests.get(url).content
    return prediction(image_bytes, model_name)