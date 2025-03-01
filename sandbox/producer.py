import json
import uuid
from confluent_kafka import Producer

import os
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")

producer_conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

request_id = str(uuid.uuid4())
image_url = 'https://www.example.com/image.jpg'

producer.produce('new', key='file', value=json.dumps({"request_id": request_id, "image_url": image_url}), callback=delivery_report)
producer.flush()