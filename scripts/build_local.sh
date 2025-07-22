#!/bin/sh

cd ..

docker build \
-t killiankopp/api-object-detection:dev \
--platform=linux/amd64 \
.