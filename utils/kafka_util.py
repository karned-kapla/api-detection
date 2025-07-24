import json
from common_api.services.v0 import Logger
from confluent_kafka import Producer

from config import KAFKA_HOST, KAFKA_PORT

logger = Logger()


class KafkaProducer:
    def __init__( self ):
        self.producer = Producer({'bootstrap.servers': f"{KAFKA_HOST}:{KAFKA_PORT}"})
        logger.connect("Connecting to Kafka")

    def send_message( self, topic, message ):
        try:
            self.producer.produce(topic=topic, key='file', value=json.dumps(message))
            self.producer.flush()
            logger.send(f"Message send to '{topic}'")
        except Exception as e:
            logger.error(f"Error while sending Kafka message: {e}")
