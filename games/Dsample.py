import os
import sys
import cv2
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# import modules.SmartphOto as SmartphOto
import modules.DeskOto as DeskOto

class DSample(DeskOto.DeskOto):
    def __init__(self, temp_dir, capture_dir, search_th):
        super().__init__(temp_dir=temp_dir, capture_dir=capture_dir, search_th=search_th)

    def main_Sequential(self):

        while 1:

            # --------------------------------------------
            # sample tap
            #
            self.tap_temp_image5_Sequential(r"image\sample\Dsample.jpg", th=0.8)

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
    D2P = DSample(temp_dir=temp_dir, capture_dir=capture_dir, search_th=0.7)

    # =================================================
    # capture image
    #
    D2P_flag, D2P_image = D2P._capture_screen()
    print("D2P_flag :{}".format(D2P_flag))
    print("D2P_image:{}".format(D2P_image.shape))

    if(D2P_flag==1):
        cv2.imwrite('image/_capture/D2P_image_sample.jpg', D2P_image)

    # ---------------------------------------------------
    # main
    #
    D2P.main_Sequential()

