import sys
import cv2 as cv
import numpy as np
import keyboard
import time
sys.path.append('D:/Rb data/Rb_codes_YHLee/ToFcam/')
try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from TLCam.windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None
from thorlabs_tsi_sdk.thorlabs_tsi_sdk.tl_camera import TLCameraSDK

class TLCam() : 
    def __init__(self, expTus=32800, fpt=1, opmode=1, trigpol=0, EEP=0) :
        self.expTus=expTus
        self.fpt=fpt
        self.opmode=opmode
        self.trigpol=trigpol
        self.EEP=EEP
        print('')
        self.camera_sdk=TLCameraSDK() 
        self.available_cameras = self.camera_sdk.discover_available_cameras()
        self.camera=self.camera_sdk.open_camera(self.available_cameras[0])
        if len(self.available_cameras) < 1:
            raise ValueError("no cameras detected")
        else:
            print('camera connected - S/N %s' %self.available_cameras)

        self.camera.exposure_time_us=self.expTus
        self.camera.frames_per_trigger_zero_for_unlimited = self.fpt
        self.camera.operation_mode = self.opmode
        self.camera.trigger_polarity = self.trigpol
        self.camera.EEP_STATUS = self.EEP
        print('   EXPOSURE_TIME_us =',self.camera.exposure_time_us)
        print('   FRAMES_PER_TRIGGER =',self.camera.frames_per_trigger_zero_for_unlimited)
        print('  ',self.camera.operation_mode)
        print('  ',self.camera.trigger_polarity)
        print('')
    

    def waitfortrig(self,shotnum=0):
        self.camera.image_poll_timeout_ms = 20
        self.camera.arm(2)
        frame=None
        if shotnum==1:
            shotnum='1st f'
        elif shotnum==2:
            shotnum='2nd f'
        elif shotnum==3:
            shotnum='3rd f'
        else:
            shotnum='F' 
        # print("Waiting for trigger...")
        while frame==None:
            frame = self.camera.get_pending_frame_or_null()
            time.sleep(0.1)
            if keyboard.is_pressed("pause"):
                frame=0
        if frame==0:
            print('"Pause\Break" key input captured.')
            if self.camera._disposed == False:
                self.camera.disarm()
                self.camera._sdk.tl_camera_close_camera(self.available_cameras[0])
                self.camera.dispose()
            if self.camera._disposed == True:
                    print("TLCam SDK closed. Exit program.")
            exit()

        

            
        elif frame is not None:
            print('%srame recieved' %shotnum)
        else:
            raise ValueError("No frame arrived")
        
        img=np.copy(frame.image_buffer).astype(int)
        self.camera.disarm()
        return img



    # def __del__(self) :
    #     self.camera._sdk.tl_camera_close_camera(self.available_cameras[0])
    #     self.camera.dispose()
    #     print("TLCam SDK closed")

