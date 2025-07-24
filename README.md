# api-detection

## Description
Simple API to manage detections.

## Requirements
Install requirements:
```bash
pip install -r requirements.txt
```

## Docs
Visit [url]/docs to see the API documentation.

## References
https://fastapi.tiangolo.com/fr/tutorial/first-steps/

## lancer l'API en local
```sh
docker run -d \
--name api-detection \
-p 8000:8000 \
-v $(pwd):/app \
-e KEYCLOAK_HOST=https://iam.karned.bzh \
-e KEYCLOAK_REALM=Karned \
-e KEYCLOAK_CLIENT_ID=karned \
-e KEYCLOAK_CLIENT_SECRET=chut! \
-e REDIS_HOST=redis \
-e REDIS_PORT=6379 \
-e REDIS_DB=0 \
-e REDIS_PASSWORD=chut! \
killiankopp/api-detection:latest
```
`
## lancer un MongoDB en local
```sh 
docker run -d \
--name mongodb-api-detection \
-p 27017:27017 \
-v ./_mongo_data:/data/db \
mongo
```