#!/usr/bin/env bash

cd ..
docker-compose -f docker-compose-test.yaml up --build
docker-compose down