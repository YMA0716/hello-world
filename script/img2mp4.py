import cv2
import os
from datetime import datetime
import glob
 

imgDir = "/home/linjz/workspace/tools/py_process/a/"
mp4SavePath = "/home/linjz/workspace/tools/py_process/a/test.mp4"
fps = 25
video_width, video_height = 1920, 1080

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
videoWriter = cv2.VideoWriter(mp4SavePath, fourcc, fps, (video_width, video_height))
imgs = glob.glob(imgDir + "/*.jpg")
for i in range(5719, 6778):#选取第..张到..张组成mp4
    print("{}/{}.jpg".format(imgDir, i))
    if os.path.isfile("{}/{}.jpg".format(imgDir, i)):
        print("{}/{}.jpg".format(imgDir, i))
        frame = cv2.imread("{}/{}.jpg".format(imgDir, i))
        videoWriter.write(frame)
videoWriter.release()
