import cv2 as cv
import numpy as np

class Classifier:
  # Init.
  def __init__(
    self,
    det_threshold = 0.5,
    classes_of_interest = None,
    frame_skip = 4,
    model_file = 'net/yolov3.weights',
    config_file = 'net/yolov3.cfg',
    classes_file = 'net/object_detection_classes_yolov3.txt'):

    self._det_threshold = det_threshold
    self._frame_skip = frame_skip

    # Create the network.
    self._net = cv.dnn.readNet(model_file, config_file, 'darknet')
    self._net.setPreferableBackend(cv.dnn.DNN_BACKEND_DEFAULT)
    self._net.setPreferableTarget(cv.dnn.DNN_BACKEND_DEFAULT)
    self._output_names = self._net.getUnconnectedOutLayersNames()

    # Read the classes.
    with open(classes_file, 'rt') as f:
      self._classes = f.read().rstrip('\n').split('\n')

    if classes_of_interest is None:
      self._classes_of_interest = self._classes
    else:
      self._classes_of_interest = classes_of_interest

  # Run each frame of a video through the network and return an array of
  # classification objects.  Each object has the class, confidence, and frame
  # number.
  def classify(self, video_file):
    frame_num = 0
    classifications = []

    # Open the capture from a video file (it should be in the video directory).
    cap = cv.VideoCapture(video_file)

    # Read one frame at a time.
    has_frame, frame = cap.read()

    while has_frame:
      # Frames are skipped for efficiency.
      if frame_num % self._frame_skip == 0:
        # Run the frame through the network.
        blob = cv.dnn.blobFromImage(frame, scalefactor=1/255)
        self._net.setInput(blob)
        outputs = self._net.forward(self._output_names)

        for output in outputs:
          for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            class_name = self._classes[class_id]
            confidence = scores[class_id]

            # If this is a class of interest and the threshold is high enough,
            # keep it.
            if class_name in self._classes_of_interest and confidence > self._det_threshold:
              classifications.append({
                'class': class_name,
                'confidence': confidence * 100,
                'frame': frame_num
              })

              # Early out.  If there is even one frame of interest, then the
              # video is kept.
              return classifications

      has_frame, frame = cap.read()
      frame_num = frame_num + 1

    return classifications
