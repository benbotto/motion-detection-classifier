#!/bin/bash

docker rmi avejidah/python3-opencv-rabbitmq-dev
docker build \
  --no-cache \
  -t avejidah/python3-opencv-rabbitmq-dev .

docker push avejidah/python3-opencv-rabbitmq-dev:latest
