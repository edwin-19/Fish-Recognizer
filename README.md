# Fish Recognizer
## Dependencies 
- Keras
- Tensorflow (1.9)
- Opencv
- PIL

# How to use
Clone this respository
```sh
git clone https://github.com/edwin-19/Fish-Recognizer.git
```

Donwload weights from [here](https://drive.google.com/open?id=1B50WdnIETk4_dIM0icrqTHQhn4XFYdas) 

Then change path for weights in yolo.py for files

Then run the following command
```sh
python yolo_video.py --input input/out.mp4 --output output/test.avi
```

# Sample Output
![Output Result](https://github.com/edwin-19/Fish-Recognizer/blob/master/output/output.jpg?raw=true "Title")

# TODO
- [ ] - Increase accuracy on detector
- [ ] - Add SORT Algorithm 
- [ ] - Add recognizer for fish

# Acknowledgement
This repo was heavily insipred by the following repos do check out their work if your interested:

- https://github.com/qqwweee/keras-yolo3
- https://github.com/Qidian213/deep_sort_yolov3

I borrowed the weights trained by the following repo to label some of the data:
- https://github.com/kwea123/fish_detection