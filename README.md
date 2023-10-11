# FRC ML Scouting

This repo is an attempt at using object detection from VODs provided by [The Blue Alliance](https://www.thebluealliance.com/) to gain statistical insights beyond the conventional FIRST API. 

## Dataset
The dataset can be found [here](https://app.roboflow.com/robotdetect/robot-detect-ckwwl/). The current dataset focuses on FIM competitions in particular for consistency in camera conditions. Could use more diversity in the dataset for better robot detection.


## Notes on Scripts and Environment Compatibility

Programs require you to input absolute paths at the moment. Currently only supports running on Ubuntu, likely not too hard to hack it to work on other operating systems though.

I reccommend looking over the [Yolov8 docs](https://docs.ultralytics.com/) for more info on how training and implementation of the neural network is handled.
