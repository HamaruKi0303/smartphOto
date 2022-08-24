# smartphOto

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
------------- ---------
certifi       2022.6.15
numpy         1.23.2
opencv-python 4.6.0.66
pip           22.1.2
setuptools    63.4.1
wheel         0.37.1
wincertstore  0.2
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


