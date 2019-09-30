import os
import pika
import json

from classifier import Classifier

# This class is used to classify (detect objects in) the videos.
classifier = Classifier(
  det_threshold = float(os.environ['DET_THRESHOLD']),
  classes_of_interest = json.loads(os.environ['CLASSES_OF_INTEREST']),
  frame_skip = int(os.environ['FRAME_SKIP']))

# Connect to rabbitmq (the container name is "mq").
connection = pika.BlockingConnection(pika.URLParameters(os.environ['MQ_CONNECTION_STRING']))
channel    = connection.channel()

# Create the queues if they have not already been created.
# The API server publishes messages on the first queue.
# The python script responds on the second queue.
channel.queue_declare(queue=os.environ['MQ_NOTIFY_QUEUE'])
channel.queue_declare(queue=os.environ['MQ_SAVE_QUEUE'])

# Fires when a message is received.  The message will contain a
# MotionRecording entity (see the motion-detection-api).  The entity
# has a video file name, which is classified.
def on_message_received(channel, method_frame, header_frame, body):
  print('Received a message.')
  print(body)
  recording = json.loads(body)['data']
  print(recording)

  # Classify the video.
  classifications = classifier.classify(
    os.environ['VIDEO_DIR'] + '/' + recording['fileName'])

  print(classifications)

  # Acknowledge the message.
  channel.basic_ack(delivery_tag=method_frame.delivery_tag)

  # Respond to the API server.
  '''
  resp = {
    'pattern': 'save_classifications',
    'data': {
      'id': recording['id'],
      'classifications': [
        {
          'class': 'person',
          'confidence': 98.6,
          'frame': 1
        }
      ]
    }
  };
  channel.basic_publish(exchange='', routing_key='save_classifications_queue', body=json.dumps(resp))
  '''

# Wire up the message listener.
channel.basic_consume(queue='classify_recordings_queue', on_message_callback=on_message_received)

try:
  print('Waiting for messages.')
  channel.start_consuming()
except KeyboardInterrupt:
  # Tear down the connection.
  print('Closing connection to RabbitMQ.')
  connection.close()
