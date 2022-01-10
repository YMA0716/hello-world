'''
从固定位置裁剪图像
'''
import os
from PIL import Image


imgDir = '/home/myl/myl/biaozhu/fake_img/'
imgSaveDir = '/home/myl/myl/biaozhu/newFake_img/'
#左上角和右下角的位置
x1 = 814
y1 = 333
x2 = 1235
y2 = 1296
imgfiles = os.listdir(imgDir)
for imgfile in imgfiles:
    img = Image.open(imgDir + imgfile)
    box1 = (x1, y1, x2, y2)  # 设置图像裁剪区域 (x左上，y左上，x右下,y右下)
    newimg = img.crop(box1)  # 图像裁剪
    imgSavePath = imgSaveDir + imgfile
    newimg.save(imgSavePath)
