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

cd build_scripts

# - Serve
/bin/bash build_and_test.sh || exit 1

# push
if [ $REGISTRY != 'localhost' ]
  then
    docker push $IMAGE_TAG
fi

/bin/bash deploy.sh || exit 1