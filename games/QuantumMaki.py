import os
import sys
import cv2
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import modules.SmartphOto as SmartphOto

class QuantumMaki(SmartphOto.SmartphOto):
    def __init__(self, device_id, adb_exe_path, temp_dir, capture_dir, search_th):
        super().__init__(device_id=device_id, adb_exe_path=adb_exe_path, temp_dir=temp_dir, capture_dir=capture_dir, search_th=search_th)

    def main_Sequential(self):

        while 1:

            # --------------------------------------------
            # sample tap
            #
            
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\ok.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\ok2.jpg", th=0.8)
            
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\choice_stage.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\battle_start.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\skip.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\skip2.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\back.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\back.png", th=0.8)
            
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\scenario.jpg", th=0.8)
            
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\new_stage.png", th=0.8)
            self.tap_temp_image5_Sequential(r"image\QuantumMaki\new_stage2.jpg", th=0.8)
            
            time.sleep(2)


if __name__ == "__main__":

    # ---------------------------------------------------
    # init
    #
    adb_exe_path    = r"D:\Local_Project\5000_HaMaruki\5000.003_smartphOto\smartphOto\sdk\platform-tools_r33.0.2-windows\platform-tools\adb.exe"
    device_id       = "d7b42150"
    temp_dir        = r"image\QuantumMaki"
    capture_dir     = r"image\_capture"

    # ---------------------------------------------------
    # connect smartphone 2 pc
    #
    S2P = QuantumMaki(device_id=device_id, adb_exe_path=adb_exe_path, temp_dir=temp_dir, capture_dir=capture_dir, search_th=0.7)

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


