import json
from confluent_kafka import Producer

import os
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")

producer_conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(producer_conf)

def send_message(topic, message):
    producer.produce(
        topic=topic,
        key='file',
        value=json.dumps(message)
    )
    producer.flush()