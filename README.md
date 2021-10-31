# 025_convert_video_to_time-lapse
![](https://img.shields.io/badge/type-python3-brightgreen)  ![](https://img.shields.io/badge/windows%20build-passing-brightgreen) ![](https://img.shields.io/badge/license-MIT-brightgreen)   
![](https://img.shields.io/badge/libraly-OpenCV-blue)

## DEMO
### You can convert your video to time-lapse(mp4).  
<img src="https://user-images.githubusercontent.com/44888139/139433664-940ce14c-3ef8-4d24-9804-0b45023a3f23.png" height="300px">  

## Features
When creating a time-lapse video(mp4), you can enter the elapsed time and text on the screen. 

### specification
- Create a single time-lapse from multiple videos.
- can set skip frames for time-lapse.
- displays elapsed time.
- can display text.
- can specify the number of pixels and FPS of the output video file.

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
  - time


## Usage
1. Put videos in the same folder.
1. Start this program.


## Acknowledgements
This program was created with reference to the following website.

- ATOM Camの常時記録動画からタイムラプス動画を生成するPythonスクリプトを書いてみた
- https://zenn.dev/yuyakato/articles/a10ad941488e60

## License
This program is under MIT license.  

# 【日本語】

## 機能
複数のビデオから一つのタイムラプスを作成します。
- 仕様
  - スキップするフレームを指定できます。
  - 経過時間と任意の文字列を表示させることができます。
  - 出力するビデオの画素、fpsの設定ができます。

## 必要なもの
Python 3
- このプログラムは、Python 3.9とWindows10で動作確認しています。

## 使い方
1. 同じフォルダに複数のビデオを置きます。
1. プログラムを実行します。


## 謝辞
このプログラムは以下のHPを参考に作成されました。

- ATOM Camの常時記録動画からタイムラプス動画を生成するPythonスクリプトを書いてみた
- https://zenn.dev/yuyakato/articles/a10ad941488e60

## ライセンス
本プログラムは、MITライセンスです
