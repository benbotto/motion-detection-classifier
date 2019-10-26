import os
import json
import time

from classifier import Classifier

classifier = Classifier(
  det_threshold = float(os.environ['DET_THRESHOLD']),
  classes_of_interest = json.loads(os.environ['CLASSES_OF_INTEREST']),
  frame_skip = int(os.environ['FRAME_SKIP']),
  model_file = os.environ['NET_MODEL_FILE'],
  classes_file = os.environ['NET_CLASSES_FILE'])

classifier.classify('./data/2019-09-26_15-13-30_290.mp4')
start = time.time()
classifier.classify('./data/2019-09-26_15-13-30_290.mp4')
print('{}s'.format(time.time() - start))
