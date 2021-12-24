
# 025_convert_video_to_time-lapse

![python3](https://img.shields.io/badge/type-python3-brightgreen)  ![passing](https://img.shields.io/badge/windows%20build-passing-brightgreen) ![MIT](https://img.shields.io/badge/license-MIT-brightgreen)  
![OpenCV](https://img.shields.io/badge/libraly-OpenCV-blue)

## DEMO

### You can convert your videos to time-lapse(mp4).  

<img src="https://user-images.githubusercontent.com/44888139/139433664-940ce14c-3ef8-4d24-9804-0b45023a3f23.png" height="300px">  

## Features

When creating a time-lapse video(mp4) from videos, you can enter the elapsed time and text on the screen. 

### specification

- Create a single time-lapse from multiple videos.
- Can set skip frames for time-lapse.
- Displays elapsed time.
- Can display text.
- Can specify the number of pixels and FPS of the output video file.

## Requirement  

Python 3

- I ran this program with the following execution environment.
  - Python 3.9
  - Windows 10

Python Library

- cv2(OpenCV)
- pathlib
- queue
- threading
- json

## Usage

1. Put videos in the same folder.
1. Write parameters to the setting.json
1. Start this program.

## Acknowledgements

This program was created with reference to the following website.
