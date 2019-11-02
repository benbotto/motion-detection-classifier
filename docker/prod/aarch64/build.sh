#!/bin/bash

if [ "$1" = "" ]
then
  echo "Usage: $0 <tag>"
  exit 1
fi

TAG=$1

docker build \
  --build-arg SSH_PRIVATE_KEY="$(<~/.ssh/id_rsa)" \
  --build-arg TAG="${TAG}" \
  -t avejidah/motion-detection-classifier:latest .

docker push avejidah/motion-detection-classifier:latest

docker tag avejidah/motion-detection-classifier:latest avejidah/motion-detection-classifier:${TAG}
docker push avejidah/motion-detection-classifier:${TAG}
