# This is just a wrapper class that's used to classify a video and store the
# results.  It's used because the classification happens in a thread, and this
# effectively holds the return value.
class ClassifierContainer:
  def __init__(self, classifier):
    self.classifier = classifier
    self.classifications = None

  def classify(self, video_file):
    self.classifications = self.classifier.classify(video_file)
