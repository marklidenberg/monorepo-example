#!/usr/bin/env bash

# - cd into project
cd ..

# - Init configuration
REGISTRY=${REGISTRY:-localhost}
IMAGE_NAME=${IMAGE_NAME:-hello-world}
SUFFIX=${IMAGE_SUFFIX:-local}
PLATFORM=${PLATFORM:-linux/arm64/v8}
#PLATFORM=${PLATFORM:-linux/amd64}

# - Get image tag
if [ $SUFFIX ]
then
	COMMIT_ID=$(python ../../../../tools/get_commit_id.py --suffix $SUFFIX)
else
  COMMIT_ID=$(python ../../../../tools/get_commit_id.py)
fi

IMAGE_TAG=$REGISTRY/$IMAGE_NAME-$COMMIT_ID

# - Run tests
IMAGE_TAG=$IMAGE_TAG docker-compose -f docker-compose.yaml up -d