# smartphOto (β版)


正式版になり次第，note等で販売する予定です．
![](https://github.com/HamaruKi0303/smartphOto/blob/main/doc/structure2.png)



## 環境の構築

### 仮想環境の作成
```
conda create -n smartphOto_v1 python=3.8
```

### 仮想環境に入る
```
conda activate smartphOto_v1
```

**仮想環境の一覧表示**
（仮想環境の名前を忘れたときに必要）
```
conda info -e
```


### 必要パッケージのインストール

```
pip install opencv-python
pip install pandas
pip install matplotlib
```

### 確認コード

```python

# -*- coding: utf-8 -*-
import cv2
import numpy as np

import subprocess
import numpy
import cv2

from datetime import datetime as dt
import time

print("Hello !!!!")

```

以下の出力が出れば問題なし．
```
(smartphOto_v1) D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto>python modules\Demo.py
Hello !!!!
```

### パッケージリスト

以下のパッケージがインストールされているはず

```
(smartphOto_v1) D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto>pip list
Package       Version
--------------- ---------
certifi         2022.6.15
cycler          0.11.0
fonttools       4.37.0
kiwisolver      1.4.4
matplotlib      3.5.3
numpy           1.23.2
opencv-python   4.6.0.66
packaging       21.3
pandas          1.4.3
Pillow          9.2.0
pip             22.1.2
pyparsing       3.0.9
python-dateutil 2.8.2
pytz            2022.2.1
setuptools      63.4.1
six             1.16.0
wheel           0.37.1
wincertstore    0.2
```



## スマホと接続

### デバイス一覧

```
adb devices
```

```
(smartphOto_v1) D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto>.\sdk\platform-tools_r33.0.2-windows\platform-tools\adb devices 
* daemon not running; starting now at tcp:5037
* daemon started successfully
List of devices attached
d7b42150        unauthorized
```

### 画面タップ

#### テンプレート

```
adb -s {シリアル} shell input touchscreen tap x y
```

#### 実行コマンド

```
.\sdk\platform-tools_r33.0.2-windows\platform-tools\adb -s d7b42150 shell input touchscreen tap 300 300
```


### 画面キャプチャー

#### テンプレート

```
adb -s {シリアル} shell screencap -p /sdcard/screenshot.png
```

```
adb -s {シリアル} pull /sdcard/screenshot.png ~/Desktop/
```

#### 実行コマンド

```
.\sdk\platform-tools_r33.0.2-windows\platform-tools\adb -s d7b42150 shell screencap -p /sdcard/screenshot.png
```

```
(smartphOto_v1) D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto>.\sdk\platform-tools_r33.0.2-windows\platform-tools\adb -s d7b42150 pull /sdcard/screenshot.png image\_capture\
/sdcard/screenshot.png: 1 file pulled, 0 skipped. 15.8 MB/s (87028 bytes in 0.005s)
```


![](https://i.imgur.com/IJYv4GC.jpg)

![](https://github.com/HamaruKi0303/smartphOto/blob/main/image/_capture/screenshot_demo.png)


## サンプルコード

```python
import os
import sys
import cv2
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import modules.SmartphOto as SmartphOto

class Sample(SmartphOto.SmartphOto):
    def __init__(self, device_id, adb_exe_path, temp_dir, capture_dir, search_th):
        super().__init__(device_id=device_id, adb_exe_path=adb_exe_path, temp_dir=temp_dir, capture_dir=capture_dir, search_th=search_th)

    def main_Sequential(self):

        while 1:

            # --------------------------------------------
            # sample tap
            #
            self.tap_temp_image5_Sequential(r"image\sample\back.png", th=0.8)

            time.sleep(2)


if __name__ == "__main__":

    # ---------------------------------------------------
    # init
    #
    adb_exe_path    = r"D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto\sdk\platform-tools_r33.0.2-windows\platform-tools\adb.exe"
    device_id       = "d7b42150"
    temp_dir        = r"image\sample"
    capture_dir     = r"image\_capture"

    # ---------------------------------------------------
    # connect smartphone 2 pc
    #
    S2P = Sample(device_id=device_id, adb_exe_path=adb_exe_path, temp_dir=temp_dir, capture_dir=capture_dir, search_th=0.7)

    # =================================================
    # capture image
    #
    S2P_flag, S2P_image = S2P._capture_screen()
    print("S2P_flag :{}".format(S2P_flag))
    print("S2P_image:{}".format(S2P_image.shape))

    if(S2P_flag==1):
        cv2.imwrite('image/_capture/S2P_image_sample.jpg', S2P_image)

    # ---------------------------------------------------
    # main
    #
    S2P.main_Sequential()


```

```bash
(smartphOto_v1) D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto>python games\sample.py

************************ temp_list *************************
['image\\sample\\back.png']
S2P_flag :1
S2P_image:(1080, 2400, 3)
max value:  1.000, position: (1932, 913), temp_path: image\sample\back.png
max value:  0.290, position: (307, 348), temp_path: image\sample\back.png
max value:  0.305, position: (1047, 305), temp_path: image\sample\back.png
```


# Desk0to

＊デスクトップゲーム用のモジュールです．

## 環境の構築

### 必要パッケージのインストール

```
pip install pyautogui
```

