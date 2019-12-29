# Fish Recognizer
## Dependencies 
- Keras
- Tensorflow (1.9)
- Opencv
- PIL

# How to use
Clone this respository
Donwload weights from here 
Then change path for weights in yolo.py for files
Then run the following command
'''sh
python yolo_video.py --input input/out.mp4 --output output/test.avi
'''
- Weights TBA

# TODO
[ ] - Increase accuracy on detector
[ ] - Add SORT Algorithm 
[ ] - Add recognizer for fish

# Acknowledgement
This repo was heavily insipred by the following repos do check out their work if your interested:

https://github.com/qqwweee/keras-yolo3
https://github.com/Qidian213/deep_sort_yolov3

I borrowed the weights trained by the following repo to label some of the data:
https://github.com/kwea123/fish_detection