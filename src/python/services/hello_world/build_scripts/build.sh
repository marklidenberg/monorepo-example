#!/usr/bin/env bash

cd ..
docker-compose -f docker-compose.yaml up --build


REGISTRY=${REGISTRY:-registry.deeplay.io/data/pyflink_parser:release-0.0.77}

docker build --platform linux/amd64 -t $REGISTRY .
docker push $REGISTRY
