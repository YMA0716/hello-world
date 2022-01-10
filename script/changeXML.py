'''
修改xml的一部分内容，并且用新的名字保存在新的文件夹
'''
import os
import cv2
import xml.etree.ElementTree as ET
import shutil
import numpy as np


xmlDir = '/home/linjz/workspace/projects/xingcheng/VOC2007/xcAnnotations/'
imgDir  = '/home/linjz/workspace/projects/xingcheng/VOC2007/xcJPEGImages/'
xmlSaveDir = '/home/linjz/workspace/projects/xingcheng/VOC2007/Annotations/'
imgSaveDir  = '/home/linjz/workspace/projects/xingcheng/VOC2007/JPEGImages/'

xmlfiles = os.listdir(xmlDir)
count = 13944
for xmlfile in xmlfiles:
    imgPath = imgDir + xmlfile[0:-3] + 'jpg'
    if os.path.exists(imgPath):
        newImgName = str(count) + '.jpg'
        newXmlName = str(count) + '.xml'
        xmlPath = xmlDir + xmlfile
        xmlSavePath = xmlSaveDir + newXmlName
        shutil.copy(xmlPath,xmlSavePath)
        tree = ET.parse(xmlSavePath)  # 打开文件    #objs=tree.findall('object')
        root = tree.getroot()
        root.find('filename').text = newImgName
        #root的孙子节点等
        for child_root in root:#遍历root的节点
            if child_root.tag == 'object':#如果是object节点
                listobject = dict()
                for xylabel in child_root:#白能力该节点下的节点
                    if xylabel.tag == 'name':
                        xylabelname = xylabel.text
                        if xylabelname == 'sideperson':
                            xylabel.text = 'person'

        tree.write(xmlSavePath)


        im = cv2.imread(imgPath)
        imgSavePath = imgSaveDir + newImgName
        cv2.imwrite(imgSavePath, im)
        count = count+1
    print(xmlfile,'finish')