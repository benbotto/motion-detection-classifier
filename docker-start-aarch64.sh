#!/bin/bash

docker run \
  --rm \
  --runtime nvidia \
  -it \
  -v `pwd`:/py/dev \
  -v /media/motion/videos:/media/motion/videos \
  --workdir /py/dev \
  --env-file ./docker/motion-detection-classifier.env \
  --name motion-detection-classifier-dev \
  avejidah/py3-tf2-opencv4:1.0.0 \
  bash
