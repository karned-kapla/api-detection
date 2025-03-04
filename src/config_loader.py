import os
import json
import logging

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du fichier de configuration: {e}")
        config = {}

    return {
        'bootstrap.servers': os.getenv('KAFKA_BROKER', config.get("bootstrap_servers", "kafka:9092"))
    }