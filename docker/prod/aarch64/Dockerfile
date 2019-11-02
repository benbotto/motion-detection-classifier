# This image is used to clone the repo, pull the yolov3 weights, and convert
# them for use with tf2.
FROM avejidah/py3-tf2-opencv4:1.0.0 as build

WORKDIR /var/motion

ARG TAG
ARG SSH_PRIVATE_KEY

# Install git and wget.
RUN apt-get update \
  && apt-get install -qq -y git wget \
  && rm -rf /var/lib/apt/lists/*

# Clone the motion-detection-classifier repo and checkout the supplied tag.
RUN mkdir /root/.ssh/ \
  && echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa \
  && chmod 600 /root/.ssh/id_rsa \
  && touch /root/.ssh/known_hosts \
  && ssh-keyscan github.com >> /root/.ssh/known_hosts \
  && git clone git@github.com:benbotto/motion-detection-classifier.git . \
  && git checkout ${TAG}

# Get the weights files and extract them to the net folder.
RUN wget -q https://github.com/benbotto/motion-detection-classifier/releases/download/tf2/yolov3.weights.tgz -O /tmp/yolov3.weights.tgz \
  && tar -zxf /tmp/yolov3.weights.tgz --directory ./net \
  && rm -f /tmp/yolov3.weights.tgz

# This is the production image with all the dependencies installed.
FROM avejidah/py3-tf2-opencv4:1.0.0

WORKDIR /var/motion

# This is used to wait for RabbitMQ.
COPY ./wait-for ./

COPY --from=build /var/motion/*.py ./
COPY --from=build /var/motion/net ./net
COPY --from=build /var/motion/yolov3_tf2 ./yolov3_tf2
COPY --from=build /var/motion/data ./data

# Add the py user with id 1000.
# Install the RabbitMQ client, pika.
# Set up wait-for (needs netcat).
RUN adduser --disabled-password --gecos '' --uid 1000 py \
  && python -m pip install --upgrade pika \
  && chmod +x ./wait-for \
  && apt-get update \
  && apt-get install -qq -y netcat \
  && rm -rf /var/lib/apt/lists/*

# Wait for RabbitMQ to come online, then run the messenger.
USER py
CMD ./wait-for -t 600 ${MQ_HOST}:${MQ_PORT} -- python ./messenger.py
