import os
import pika
import json
from threading import Thread

from classifier import Classifier
from classifier_container import ClassifierContainer

# This class is used to classify (detect objects in) the videos.
classifier = Classifier(
  det_threshold = float(os.environ['DET_THRESHOLD']),
  classes_of_interest = json.loads(os.environ['CLASSES_OF_INTEREST']),
  frame_skip = int(os.environ['FRAME_SKIP']),
  model_file = os.environ['NET_MODEL_FILE'],
  classes_file = os.environ['NET_CLASSES_FILE'])

# Connect to rabbitmq (the container name is "mq").
mq_conn_str = 'amqp://{}:{}'.format(os.environ['MQ_HOST'], os.environ['MQ_PORT'])
connection  = pika.BlockingConnection(pika.URLParameters(mq_conn_str))
channel     = connection.channel()

# Create the queues if they have not already been created.
# The API server publishes messages on the first queue.
# The python script responds on the second queue.
channel.queue_declare(queue=os.environ['MQ_NOTIFY_QUEUE'])
channel.queue_declare(queue=os.environ['MQ_SAVE_QUEUE'])

# Fires when a message is received.  The message will contain a
# MotionRecording entity (see the motion-detection-api).  The entity
# has a video file name, which is classified.
def on_message_received(channel, method_frame, header_frame, body):
  recording = json.loads(body)['data']

  # Classify the video in a thread.  A wrapper container is used to hold the
  # classifications.
  print('Classifying {}'.format(recording['fileName']))

  container = ClassifierContainer(classifier)

  thread = Thread(target = lambda: container.classify(
    os.environ['VIDEO_DIR'] + '/' + recording['fileName']))
  thread.start()

  # Let pika sleep until the classification is done.  RabbitMQ sends heartbeats
  # to check if the client is alive, and this ensures that pika responds during
  # the long-running classification process.
  while thread.is_alive():
    connection.sleep(1)

  num_objects = len(container.classifications)
  print('Found {} objects of interest.'.format(num_objects))

  # Acknowledge the message.
  channel.basic_ack(delivery_tag=method_frame.delivery_tag)

  # The recording is saved if there are objects of interest, or deleted
  # otherwise.
  if num_objects > 0:
    # The motion recording ID is expected on each classification (the
    # classifications are saved in the DB on the API side).
    for classification in container.classifications:
      classification['motionRecordingId'] = recording['id']

    # Respond to the API server with the classifications.
    resp = {
      'pattern': 'save_classifications',
      'data': container.classifications
    };

    channel.basic_publish(exchange='', routing_key=os.environ['MQ_SAVE_QUEUE'],
      body=json.dumps(resp))
  else:
    # Respond to the API server with the recording id so it can be deleted.
    resp = {
      'pattern': 'delete_motion_recording',
      'data': recording
    };

    channel.basic_publish(exchange='', routing_key=os.environ['MQ_SAVE_QUEUE'],
      body=json.dumps(resp))

# Wire up the message listener.
channel.basic_consume(queue='classify_recordings_queue', on_message_callback=on_message_received)

try:
  print('Waiting for messages.')
  channel.start_consuming()
except KeyboardInterrupt:
  # Tear down the connection.
  print('Closing connection to RabbitMQ.')
  connection.close()
