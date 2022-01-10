#按照帧数新建图像名字保存
import cv2
import os


videoDir = '/home/myl/myl/biaozhu/20220105/'
imgSaveDir = '/home/myl/myl/biaozhu/gangjuan-1/'
skipFrame = 20  # 隔多少帧保留一帧
videofiles = os.listdir(videoDir)
currentframe = 0
for videofile in videofiles:
    videoPath = videoDir+videofile
    cam = cv2.VideoCapture(videoPath)
    while (True):
        ret, frame = cam.read()  # ret是布尔型，正确读取则返回true，读取失败则返回false
        if ret: # 如果视频仍然在，继续创建图像
            if currentframe % skipFrame == 0:
                imgSavePath = imgSaveDir + str(currentframe) + '.jpg'
                print('Creating...' + imgSavePath)
                cv2.imwrite(imgSavePath, frame)
            currentframe = currentframe+1
        else:
            break
    cam.release()

    cv2.destroyAllWindows()

