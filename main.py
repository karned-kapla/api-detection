from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("models/yolo11l.pt")
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/detect/")
async def detect_objects(file: UploadFile):
    image_bytes = await file.read()
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    results = model.predict(image)

    datas = {}
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "xmin": float(box.xyxy[0][0]),
                "ymin": float(box.xyxy[0][1]),
                "xmax": float(box.xyxy[0][2]),
                "ymax": float(box.xyxy[0][3]),
                "confidence": float(box.conf[0]),
                "class": int(box.cls[0]),
                "name": model.names[int(box.cls[0])]
            })
    datas["shape"] = image.shape
    datas["boxes"] = detections
    datas["speed"] = results[0].speed
    return {"detection": datas}