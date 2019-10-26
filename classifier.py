import cv2
import numpy as np
import tensorflow as tf

from yolov3_tf2.models import YoloV3

class Classifier:
  # Init.
  def __init__(
    self,
    det_threshold = 0.5,
    classes_of_interest = None,
    frame_skip = 4,
    model_file = 'net/yolov3.weights',
    classes_file = 'net/object_detection_classes_yolov3.txt'):

    self._det_threshold = det_threshold
    self._frame_skip = frame_skip

    # Read the classes.
    with open(classes_file, 'rt') as f:
      self._classes = f.read().rstrip('\n').split('\n')

    if classes_of_interest is None:
      self._classes_of_interest = self._classes
    else:
      self._classes_of_interest = classes_of_interest

    # Create the network.
    self._net = YoloV3(classes=len(self._classes))
    self._net.load_weights(model_file)

  # Run each frame of a video through the network and return an array of
  # classification objects.  Each object has the class, confidence, and frame
  # number.
  def classify(self, video_file):
    frame_num = 0
    classifications = []

    # Open the capture from a video file.
    cap = cv2.VideoCapture(video_file)

    # Read one frame at a time.
    has_frame, frame = cap.read()

    '''
    while has_frame:
      # Frames are skipped for efficiency.
      if frame_num % self._frame_skip == 0:
        # Convert the frame to a batch (TODO: send multiple frames).
        frame = tf.expand_dims(frame, 0)

        # Yolov3 works with 416x416 images.
        frame = tf.image.resize(frame, (416, 416))

        # The pixels should be in the range 0-1 (not 0-255).
        frame = frame / 255

        # Run the frame through the network.
        boxes, scores, classes, nums = self._net.predict(frame)

        for i in range(nums[0]):
          class_id = int(classes[0][i])
          class_name = self._classes[class_id]
          confidence = scores[0][i]

          print('Frame Num: {} Class: {} Score: {:.4f}'.format(frame_num, class_name, confidence))

          if class_name in self._classes_of_interest and confidence > self._det_threshold:
            classifications.append({
              'class': class_name,
              'confidence': confidence * 100,
              'frame': frame_num
            })

            # Early out.  If there is even one frame of interest, then the
            # video is kept.
            #return classifications

      has_frame, frame = cap.read()
      frame_num = frame_num + 1
    '''

    frames = []
    while has_frame:
      # Frames are skipped for efficiency.
      if frame_num % self._frame_skip == 0:
        frames.append(frame)

      has_frame, frame = cap.read()
      frame_num = frame_num + 1

    # Convert the frames to a numpy array so they can be fed through the network.
    frames = np.array(frames);

    # Yolov3 works with 416x416 images.
    frames = tf.image.resize(frames, (416, 416))

    # The pixels should be in the range 0-1 (not 0-255).
    frames = frames / 255

    # Run the frame through the network.
    boxes, scores, classes, nums = self._net.predict(frames)

    for i in range(len(frames)):
      for j in range(nums[i]):
        class_id = int(classes[i][j])
        class_name = self._classes[class_id]
        confidence = scores[i][j]

        print('Frame num: {} Class: {} Score: {:.4f}'.format(i, class_name, confidence))

    return classifications
