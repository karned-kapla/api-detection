#!/bin/sh

cd ..

docker run -d \
--name api-object-detection \
--network karned \
-e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
-v ".:/app" \
-p 8011:8000 \
killiankopp/api-object-detection:dev