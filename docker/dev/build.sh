#!/bin/bash

docker build \
  -t avejidah/python3-opencv4-rabbitmq-tensorflow2-dev .

docker push avejidah/python3-opencv4-rabbitmq-tensorflow2-dev:latest
