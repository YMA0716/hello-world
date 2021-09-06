import cv2
import os
import numpy as np
from PIL import Image
# import torch

imgDir ="/home/myl/myl/py_process/myl/testdata/"
files = os.listdir(imgDir)


model_weights = "graph300.pbtxt"
model_config = "person300x300.pb"
# 修改图片尺寸达到符合训练模型
resized_process_w = 300
resized_process_h = 300
scale = 1.0
base_thr = 0.5  # 像人的概率
nms_thr = 0.5  # 像人范围重叠的概率
net = cv2.dnn.readNet(model_weights, model_config)


j = 0
for file in files:
    frame = cv2.imread(os.path.join(imgDir, file))
    size = frame.shape
    print(size)

    classIds = []
    boxes = []
    confidences = []  # 人像概率
    # 原图和修改后的比例
    ratio_w = size[1]/resized_process_w
    ratio_h = size[0]/resized_process_h
    frame1 = cv2.resize(frame,(resized_process_h, resized_process_w))
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    ###
    inputBlob = cv2.dnn.blobFromImage(frame1, scale, (resized_process_h, resized_process_w), (0, 0, 0), False, False)
    net.setInput(inputBlob)
    out = net.forward()
    # print(out.shape)
    out = np.squeeze(out)

    len_out = out.shape[0]
    for i in range(len_out):
         result = out[i]

         confidence = result[2]
         if confidence > base_thr:
            left = result[3] * resized_process_w * ratio_w
            top = result[4] * resized_process_h * ratio_h
            right = result[5] * resized_process_w * ratio_w
            bottom = result[6] * resized_process_h * ratio_h

            width = right - left + 1
            height = bottom - top + 1

            classIds.append(result[1] - 1)
            box =[]
            box.append(int(left))
            box.append(int(top))
            box.append(int(width))
            box.append(int(height))
            boxes.append(box)
            confidences.append(float(confidence))

    boxes_id = cv2.dnn.NMSBoxes(boxes, confidences, base_thr, nms_thr)
    #此处有疑问
    for i in range(boxes_id.shape[0]):
        data = boxes[int(boxes_id[i])]
        cv2.rectangle(frame, (data[0], data[1]), (data[0]+data[2], data[1]+data[3]), (0, 255, 0), 4)
        #(0,255,0)画线对应rgb颜色， 4 所画线的宽度
        newFrame = frame[data[1]:data[1]+data[3],data[0]:data[0]+data[2]]
        cv2.imwrite('/home/myl/myl/py_process/myl/test'+ str(data[0]) +'.png', newFrame)
    cv2.imwrite('/home/myl/myl/py_process/myl/test'+ str(j) +'.png', frame)

    j = j+1

