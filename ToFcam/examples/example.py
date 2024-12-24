import sys
import cv2 as cv
import numpy as np
import keyboard
import time

CONDITION=True
CONDITION2=True

try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

sys.path.append('../thorlabs_tsi_sdk-0.0.8/')
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK

with TLCameraSDK() as camera_sdk :
    available_cameras = camera_sdk.discover_available_cameras()
    print(available_cameras)
    if len(available_cameras) < 1:
        raise ValueError("no cameras detected")
    else:
        print('camera connected - S/N %s' %available_cameras)

    with camera_sdk.open_camera(available_cameras[0]) as camera:
        camera.frames_per_trigger_zero_for_unlimited = 1  # start camera in continuous mode
        camera.operation_mode = 1
        camera.exposure_time_us=32800
        camera.trigger_polarity=0
        camera.DATA_RATE = 3
        # camera.Taps = 2
        camera.SENSOR_TYPE = 0
        camera.EEP_STATUS = 0  
        i=0

        """
            In a real-world scenario, we want to save the image width and height before color processing so that we 
            do not have to query it from the camera each time it is needed, which would slow down the process. It is 
            safe to save these after arming since the image width and height cannot change while the camera is armed.
        """
        image_width = camera.image_width_pixels
        image_height = camera.image_height_pixels

        while CONDITION==True:
            
            i=i+1

            camera.image_poll_timeout_ms = 20  # 2 second timeout    
            
            print("Waiting for New image.")
            
            camera.arm(2)     
            frame=None
            while frame==None:
                frame = camera.get_pending_frame_or_null()
                time.sleep(0.1)
                if keyboard.is_pressed("esc"):
                    frame=0
            if frame==0:
                print('"ESC" input caputured. Exit program.')
                exit()
            elif frame is not None:
                print("1st frame received!")
            else:
                raise ValueError("No frame arrived within the timeout!")
        
            img1=np.copy(frame.image_buffer).astype(int)
            camera.disarm()
        
            camera.arm(2)     
            frame=None
            while frame==None:
                frame = camera.get_pending_frame_or_null()
                time.sleep(0.1)
                if keyboard.is_pressed("esc"):
                    frame=0
            if frame==0:
                print('"ESC" input caputured. Exit program.')
                exit()
            elif frame is not None:
                print("2nd frame received!")
            else:
                raise ValueError("No frame arrived within the timeout!")

            img2=np.copy(frame.image_buffer).astype(int)

            camera.disarm()

            camera.arm(2)     
            frame=None
            while frame==None:
                frame = camera.get_pending_frame_or_null()
                time.sleep(0.1)
                if keyboard.is_pressed("esc"):
                    frame=0
            if frame==0:
                print('"ESC" input caputured. Exit the program.')
                exit()
            elif frame is not None:
                print("3rd frame received!")
            else:
                raise ValueError("No frame arrived within the timeout!")

            img3=np.copy(frame.image_buffer).astype(int)

            camera.disarm()

            img4=np.log((np.abs(img2-img3)+1))-np.log((np.abs(img1-img3)+1))
            # img1=cv.resize(img1, dsize=(0,0), fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
            # img2=cv.resize(img2, dsize=(0,0), fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
            # img3=cv.resize(img3, dsize=(0,0), fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
            # cv.imshow('img1',img1/img1.max())
            # cv.imshow('img2',img2/img2.max())
            # cv.imshow('img3',img3/img3.max())
            # cv.waitKey()
            img4=cv.resize(img4, dsize=(0,0), fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
            cv.imwrite('../imgnum'+str(i)+'.bmp',img1/img1.max()*255)
            cv.imshow('',img1/img1.max())
            cv.waitKey()
            time.sleep(0.01)
            cv.destroyAllWindows()
            time.sleep(0.01)


            




#  Because we are using the 'with' statement context-manager, disposal has been taken care of.

print("program completed")
