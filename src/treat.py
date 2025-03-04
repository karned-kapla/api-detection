import logging
import uuid

from src.config_loader import load_config
from src.kafka_producer import KafkaProducer
from src.models.input import UrlInput
from src.models.output import SendResponse


def treat_url(payload: UrlInput) -> SendResponse:
    config = load_config()
    producer = KafkaProducer(config)

    uuid_detection = str(uuid.uuid4())
    uuid_user = str(uuid.uuid4())
    uuid_entity = str(uuid.uuid4())
    uuid_credentials = str(uuid.uuid4())

    topic = config["topic"]
    message = {
        'uuid_detection': uuid_detection,
        'url': str(payload.url),
        'model_name': payload.model_name,
        'uuid_user': uuid_user,
        'uuid_entity': uuid_entity,
        'uuid_credentials': uuid_credentials
    }
    producer.send_message(topic, message)

    response = SendResponse(
        status="transmitted",
        message="The URL has been transmitted for processing.",
        uuid=uuid_detection
    )

    logging.info(f"Réponse API : {response}")
    return response