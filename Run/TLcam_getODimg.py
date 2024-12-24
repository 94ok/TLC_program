import sys; sys.path.append("..\\")
from ToFcam.TLCam.TLCamclass import *
import datetime as dt
from py_functions.catchlastfile import catchlastfile
NOW = dt.datetime.now()

CONDITION=True
i=0
currentpath="d:\\Rb data\\Data\\Raw_TLC\\"+NOW.strftime("%Y")+"\\"+NOW.strftime("%m")+"\\"+NOW.strftime("%d")+"\\"
currentpath2="d:\\Rb data\\Data\\bmpimg_TLC\\"+NOW.strftime("%Y")+"\\"+NOW.strftime("%m")+"\\"+NOW.strftime("%d")+"\\"
ToFcam=TLCam()
contrastfactor=100

while CONDITION==True:
    fname=catchlastfile(currentpath)
    print("Waiting for next image")
    if fname==None : 
        fname=NOW.strftime("%Y")[2:4]+NOW.strftime("%m")+NOW.strftime("%d")+"_1"
        imgnum=1
    else :
        imgnum=int(fname[7:-4])+1
        fname=fname[0:7]+str(imgnum)
    img1=ToFcam.waitfortrig(1)
    img2=ToFcam.waitfortrig(2)
    img3=ToFcam.waitfortrig(3)

    calimg1=img1[0:300,0:300].sum()
    calimg2=img2[0:300,0:300].sum()
    # calimg1=img1[0:300,1200:1500].sum()
    # calimg2=img2[0:300,1200:1500].sum()
    # calimg1=img1[0:100,0:100].sum()
    # calimg2=img2[0:100,0:100].sum()
    calcoeff=calimg1/calimg2
    print(calimg1, calimg2, calcoeff)

    img4=np.log((np.abs(img2*calcoeff-img3)+1))-np.log((np.abs(img1-img3)+1))
    # NoiseCutoff=10/100*img4.max()
    # for j in range(img4.shape[0]):
    #     for k in range(img4.shape[1]):
    #         if img4[j,k]<NoiseCutoff:
    #             img4[j,k]=0
    # print(img1.shape,img2.shape,img3.shape,img4.shape)
    
    rawdatfile=np.array([img1,img2,img3,img4])
    np.save(currentpath+fname,rawdatfile)
    cv.imwrite(currentpath2+fname+'.bmp',img4*contrastfactor)
    print("max pixel value : "+str(img4.max()))


    print('  Image %s is saved\n' %fname)
    # cv.imshow('',img4/img4.max())
    # cv.waitKey()
    # time.sleep(0.01)
    # cv.destroyAllWindows()
    time.sleep(0.01)