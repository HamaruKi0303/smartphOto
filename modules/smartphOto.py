# -*- coding: utf-8 -*-
import cv2
import numpy as np
import glob
import re
import os

import pprint
import subprocess
import numpy
import cv2

from datetime import datetime as dt
import time
import pandas as pd
from matplotlib import pyplot as plt

class Android2PC:

    def __init__(self, device_id, adb_exe_path, temp_dir, search_th=0.9):
        self.device_id      = device_id
        self.adb_exe_path   = adb_exe_path
        self.share_capture_image = ""
        self.temp_dir       = temp_dir
        self.temp_dict      = {}
        self.th             = 0.7
        self.search_th      = search_th

        self._load_temp_image()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # common section
    #
    def _capture_screen(self):
        '''
            スクリーンキャプチャを取るための関数
            PNG形式で取得

        Returns
        ----------
        img : opencv Mat
            OpenCV形式のイメージ

        '''

        try:
            result = subprocess.check_output([self.adb_exe_path, '-s', self.device_id, 'exec-out', 'screencap', '-p'])
            return 1, cv2.imdecode(numpy.frombuffer(result, numpy.uint8), cv2.IMREAD_COLOR)
        except:
            print("image none")
            return -1, -1

    def _tap(self, sarch_temp_key_list, temp_key):
        self._tap_PC2Android(x=sarch_temp_key_list[temp_key][0], y=sarch_temp_key_list[temp_key][1])

    def _tap_PC2Android(self, x, y):
        result = subprocess.check_output([self.adb_exe_path, '-s', self.device_id, 'shell', 'input', 'tap', str(x), str(y)])

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Sequential section
    #
    def tap_temp_image5_Sequential(self, temp_path, th=0.8):
        temp = cv2.imread(temp_path)

        capture_flag, capture_image = self._capture_screen()
        # cv2.imwrite('_screen.png', img)

        # print("capture_image.shape  :{}".format(capture_image.shape))
        # print("temp.shape           :{}".format(temp.shape))

        result = cv2.matchTemplate(capture_image, temp, cv2.TM_CCOEFF_NORMED)
        # 最も類似度が高い位置を取得する。
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        # print(temp.shape)

        print("max value: {:6.3f}, position: {}, temp_path: {}".format(maxVal, maxLoc, temp_path))

        if(maxVal < th):
            return False

        # adb shell input touchscreen tap x y
        self._tap_PC2Android(maxLoc[0]+temp.shape[1]/2, maxLoc[1]+temp.shape[0]/2)

        return True



    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Parallel section
    #
    def _load_temp_image(self):
        temp_list = glob.glob(self.temp_dir + r"\*")

        print("\n{:*^60}".format(" temp_list "))
        pprint.pprint(temp_list)

        for temp_path in temp_list:
            temp_key = temp_path.split("\\")[-1].split(".")[0]
            self.temp_dict[temp_key] = {}
            self.temp_dict[temp_key]["temp_path"] = temp_path
            self.temp_dict[temp_key]["temp_image"] = cv2.imread(temp_path)
    
    def tap_temp_image5_Parallel(self):

        sarch_temp_key_list = {}
        columns2 = ["x", "y", "maxVal"]
        detect_total_df = pd.DataFrame(data={}, columns=columns2)

        self._set_capture_screen()
        capture_flag, capture_image = self.share_capture_image
        analy_image                 = capture_image * 0.2

        # 時間計測開始
        time_sta = time.time()

        for k, v in self.temp_dict.items():
         
            result = cv2.matchTemplate(capture_image, v["temp_image"], cv2.TM_CCOEFF_NORMED)
            # cv2.imwrite('_screen_result.png', result*255)

            kernel = np.ones((30,30),np.float32)/25
            _result = result.copy()
            _result[_result<0.6] = 0
            _result = cv2.filter2D(_result,-1,kernel)
            

            analy_image[analy_image.shape[0]-result.shape[0]:analy_image.shape[0], analy_image.shape[1]-result.shape[1]:analy_image.shape[1], 2] += _result*150
            # analy_image[0:result.shape[0], 0:result.shape[1], 0] += result*100
            
            # 最も類似度が高い位置を取得する。
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
            # (px, py) = (int(maxLoc[0]+v["temp_image"].shape[1]/2), int(maxLoc[1]+v["temp_image"].shape[0]/2)),

            if(0.8 < maxVal):
                # ------------------------------------------------
                # 検出結果の描画
                #
                cv2.putText(analy_image, 
                            k, 
                            (int(maxLoc[0]), int(maxLoc[1])),
                            cv2.FONT_HERSHEY_PLAIN, 3,
                            (0, 255, 0), 
                            3, 
                            cv2.LINE_AA)
                
                cv2.rectangle(analy_image,
                            pt1=(int(maxLoc[0]), int(maxLoc[1])),
                            pt2=(int(maxLoc[0]+v["temp_image"].shape[1]), int(maxLoc[1]+v["temp_image"].shape[0])),
                            color=(0, 255, 0),
                            thickness=3,
                            lineType=cv2.LINE_4,
                            shift=0)

            sarch_temp_key_list[k] = (maxLoc[0]+v["temp_image"].shape[1]/2, maxLoc[1]+v["temp_image"].shape[0]/2, maxVal)

            _detect_df = pd.DataFrame( data = [[maxLoc[0]+v["temp_image"].shape[1]/2, maxLoc[1]+v["temp_image"].shape[0]/2, maxVal]], 
                                columns = columns2,
                                index=[k,])

            detect_total_df = pd.concat([detect_total_df, _detect_df])


        # ------------------------------------------------
        # 経過時間（秒）
        #
        tim = time.time()- time_sta
        print("Sarch time : {:6.3f}s".format(tim))
        print("-------------------------------------------")

        # ------------------------------------------------
        # デバッグ描画用
        #
        analy_image = cv2.resize(analy_image, dsize=None, fx=0.5, fy=0.5)
        cv2.imshow("Image", analy_image/255)
        k = cv2.waitKey(5) & 0xFF

        return detect_total_df

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # タップ処理
    #
    def _key_tap(self, temp_key, detect_total_df, temp_key2="", time_sleep=1):
        if(temp_key in list(detect_total_df.index)):
            
            if(temp_key2==""):
                print(">>>>>> {}".format(temp_key))
                self._tap_PC2Android(detect_total_df["x"][temp_key], detect_total_df["y"][temp_key])
                time.sleep(time_sleep)
            else:
                print(">>>>>> {} >>>>>> {}".format(temp_key, temp_key2))
                # print(detect_total_df)
                self._tap_PC2Android(detect_total_df["x"][temp_key2], detect_total_df["y"][temp_key2])
                time.sleep(time_sleep)
            return True
        
        return False

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # スマホ画面の取得
    #
    def _set_capture_screen(self):
        try:
            # 時間計測開始
            time_sta = time.time()
            
            result = subprocess.check_output([self.adb_exe_path, '-s', self.device_id, 'exec-out', 'screencap', '-p'])
            self.share_capture_image =  1, cv2.imdecode(numpy.frombuffer(result, numpy.uint8), cv2.IMREAD_COLOR)

            # 経過時間（秒）
            tim = time.time()- time_sta
            print("Set time   : {:6.3f}s".format(tim))

        except:
            print("image none")
            self.share_capture_image =  -1, -1


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 単体テスト環境
#

if __name__ == "__main__":

    # ---------------------------------------------------
    # init
    #
    adb_exe_path    = r"d:\Local_Project\6000_Polaris\002_Autoroid\sdk\platform-tools_r33.0.2-windows\platform-tools\adb.exe"
    device_id       = "f6a19bcb"
    temp_dir        = r"image\azuren"

    # ---------------------------------------------------
    # connect android 2 pc
    #
    A2P = Android2PC(device_id=device_id, adb_exe_path=adb_exe_path, temp_dir=temp_dir)

    # A2P._load_temp_image()
    # sarch_temp_key_list = A2P.tap_temp_image5_Parallel()
    # pprint.pprint(sarch_temp_key_list)



    # ---------------------------------------------------
    # capture image
    #
    A2P_flag, A2P_image = A2P._capture_screen()

    if(A2P_flag==1):
        cv2.imwrite('image/A2P_image_sample.jpg', A2P_image)
    

    raise
    


