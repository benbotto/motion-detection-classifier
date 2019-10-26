#!/bin/bash

docker run \
  --rm \
  --gpus all \
  -it \
  -v `pwd`:/py/dev \
  --workdir /py/dev \
  --env-file ./docker/motion-detection-classifier.env \
  --user 1000 \
  --name motion-detection-classifier-dev \
  avejidah/python3-opencv4-rabbitmq-tensorflow2-dev \
  bash
