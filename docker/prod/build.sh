#!/bin/bash

if [ "$1" = "" ]
then
  echo "Usage: $0 <tag>"
  exit 1
fi

TAG=$1

# Cleanup.
docker rmi avejidah/motion-detection-classifier:latest 2>/dev/null

# Build and tag as lastest.
docker build \
  --build-arg SSH_PRIVATE_KEY="$(<~/.ssh/id_rsa)" \
  --build-arg TAG="${TAG}" \
  --no-cache \
  -t avejidah/motion-detection-classifier:latest .

docker push avejidah/motion-detection-classifier:latest

# Tag with a tag matching the code repository.
docker tag avejidah/motion-detection-classifier:latest \
  avejidah/motion-detection-classifier:${TAG}
docker push avejidah/motion-detection-classifier:${TAG}
