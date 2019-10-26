yolov3.weights or yolov3-tiny.weights is needed but not included due to its
size.  Get it here: https://pjreddie.com/media/files/yolov3.weights or
https://pjreddie.com/media/files/yolov3-tiny.weights

Then the weights need to be converted to work with tensorflow.  Example:

```
wget https://pjreddie.com/media/files/yolov3.weights -O ./data/yolov3.weights
python convert.py --weights ./data/yolov3.weights --output ./net/yolov3.weights
rm ./data/yolov3.weights
```
