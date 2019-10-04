# An Ubuntu image is used to clone the repository.
FROM ubuntu:bionic as build

WORKDIR /var/py

ARG TAG
ARG SSH_PRIVATE_KEY

# Install git.
RUN apt-get update && \
    apt-get install -qq -y software-properties-common apt-utils && \
    add-apt-repository ppa:git-core/ppa && \
    apt-get update && \
    apt-get install -qq -y git wget

# Clone the motion-detection-classifier repo and checkout the supplied tag.
RUN mkdir /root/.ssh/ && \
    echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    touch /root/.ssh/known_hosts && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    git clone git@github.com:benbotto/motion-detection-classifier.git . && \
    git checkout ${TAG}

# Get the weights file.
RUN wget -q -P net/ https://pjreddie.com/media/files/yolov3.weights

# OpenCV 4 image with pika (for RabbitMQ) and a 'py' user with id 1000.
FROM jjanzic/docker-python3-opencv:opencv-4.0.1

WORKDIR /var/py

ENV PYTHONUNBUFFERED=1

# Add the py user with id 1000 and install pika, the RabbitMQ client.
RUN adduser --disabled-password --gecos '' --uid 1000 py && \
  pip3 install --upgrade pip && \
  pip3 install pika && \
  apt-get update && \
  apt-get install -qq -y netcat && \
  rm -rf /var/lib/apt/lists/*

# This is used to wait for the MQ server to come online.  It requires netcat.
COPY ./wait-for ./
RUN chmod +x wait-for

COPY --from=build /var/py/*.py ./
COPY --from=build /var/py/net ./net

# Wait for RabbitMQ to come online, then run the messenger.
USER py
CMD ./wait-for ${MQ_HOST}:${MQ_PORT} -- python3 ./messenger.py
