#change img fomat,for example png to jpg
#图像名字不变
import os
import cv2

imgDir = '/home/linjz/workspace/projects/jiangtun/data/framefor2mp4/'
imgSaveDir = '/home/linjz/workspace/projects/jiangtun/data/framefor2mp4/'
files = os.listdir(imgDir)
for file in files:
    imgPath = os.path.join(imgDir,file)
    im = cv2.imread(imgPath)
    imgNewName = file[0:-3]+'jpg'
    imgSavePath = os.path.join(imgSaveDir,imgNewName)
    cv2.imwrite(imgSavePath,im)
    print(file,'finish')