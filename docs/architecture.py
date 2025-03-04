from diagrams import Cluster, Diagram
from diagrams.onprem.client import Client
from diagrams.programming.framework import FastAPI
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx

with Diagram("API Object Detection v2 EDA", show=True, direction="TB"):
    client = Client("Client API")
    gateway = Nginx("API Gateway")
    consumer = Server("Consumer : ms-object-detection")

    with Cluster("API Object Detection v2"):
        api = FastAPI("API Object Detection")
        topic = Kafka("Topic: object-detection")

    client >> gateway >> api >> topic >> consumer