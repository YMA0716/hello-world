import cv2
import os
import filetype

imgDir = '/home/myl/myl/workspace'
newImgDir = '/home/myl/myl/workspace/photo'

files = os.listdir(imgDir)
for file in files:
    imgPath = os.path.join(imgDir, file)
    #判断文件是否是图片
    img = cv2.imread(imgPath) #读取图片
    # 判断拿到的文件是否是图片类型

    newImg = file[0:2] +".jpg"
    imgSavePath = os.path.join(newImgDir, newImg)
    cv2.imwrite(imgSavePath, img)
    print(file, "finish")
