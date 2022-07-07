#!/usr/bin/env bash

cd ..
docker-compose -f docker-compose.yaml up --build

REGISTRY=${REGISTRY:-localhost}
IMAGE_PATH=${IMAGE_PATH:-localhost}
docker build --platform linux/amd64 -t IMAGE_PATH .
docker push $IMAGE_PATH
