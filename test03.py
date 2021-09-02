import cv2
import os



input_video = '/home/myl/myl/workspace/video/'
output_dir = '/home/myl/myl/workspace/photo1/'

skipFrame = 60  #隔多少帧保留一帧 ## 驼峰命名法
videoFiles = os.listdir(input_video)  # 读取文件夹下面所有文件
currentframe = 0
for videoFile in videoFiles:
    videoPath = input_video + videoFile  # 合成路径
    cam =cv2.VideoCapture(videoPath)    #读取视频
    while(True):
        ret,frame =cam.read() # ret是布尔型，代表读取是否成功
        if ret:
            if currentframe % skipFrame == 0 :
                imgSavePath = output_dir + str(currentframe)+'.jpg'
                print('creating...'+ imgSavePath)
                cv2.imwrite(imgSavePath,frame)
            currentframe = currentframe +1
        else:
            break
    cam.release()

    cv2.destroyAllWindows()

