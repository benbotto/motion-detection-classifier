FROM tensorflow/tensorflow:2.0.0-gpu-py3

RUN apt-get update \
  && apt-get install -y libsm6 libxext6 libxrender-dev wget \
  && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' --uid 1000 py && \
  pip3 install --upgrade pip && \
  pip3 install pika opencv-python==4.1.1.26
