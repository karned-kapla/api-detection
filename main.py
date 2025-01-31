from fastapi import FastAPI, File, UploadFile
from src.yolo_detection import prediction, uri_file_prediction, url_file_prediction

app = FastAPI()


@app.post("/file")
async def detect_objects(file: UploadFile, model_name: str = "yolo11l"):
    image_bytes = await file.read()
    result = prediction(image_bytes, model_name)
    return result

@app.post("/uri")
async def detect_objects_uri(uri: str, model_name: str = "yolo11l"):
    result = uri_file_prediction(uri, model_name)
    return result

@app.post("/url")
async def detect_objects_url(url: str, model_name: str = "yolo11l"):
    result = url_file_prediction(url, model_name)
    return result