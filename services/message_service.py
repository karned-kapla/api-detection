from utils.kafka_util import KafkaProducer
from common_api.services.v0 import Logger

logger = Logger()

class MessageService:
    def __init__(self):
        self.producer = KafkaProducer()
    
    def send_detection_task(self, topic, detection_uuid, secret, url, model):
        try:
            message = {
                "uuid": detection_uuid,
                "secret": secret,
                "url": str(url),
                "model": model,
                "response": [
                    {
                        "canal": "kafka",
                        "topic": "detections_done"
                    },
                    {
                        "canal": "api",
                        "url": f"http://karned-api-detection:8000/detection/v1/tasks/results"
                    }
                ]
            }
            
            self.producer.send_message(topic=topic, message=message)
            logger.info(f"Sent detection task for UUID {detection_uuid} to topic {topic}")
        except Exception as e:
            logger.error(f"Error sending detection task: {e}")
            raise ValueError(f"Failed to send detection task: {e}")