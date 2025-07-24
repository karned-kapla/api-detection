

def detection_serial(detection) -> dict:
    return {
        "uuid": str(detection["_id"]),
        "url": detection.get("url"),
        "model": detection.get("model"),
        "status": detection.get("status"),
        "result": detection.get("result"),
        "created_by": detection.get("created_by"),
        "secret": detection.get("secret")
    }


def list_detection_serial(detections) -> list:
    return [detection_serial(detection) for detection in detections]
