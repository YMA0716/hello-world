import time

import cv2 as cv
import os
import numpy as np
import os.path as osp
from common import letterbox

mode_path = '/home/myl/data/weights/last.onnx'

class Yolov5:
    def __init__(self, model_path, classes, input_size=(640, 640),
                 confThreshold=0.5, nmsThreshold=0.5,
                 onnx_rt=False):
        self.classes = classes
        self.colors = [np.random.randint(0, 255, size=3).tolist() for _ in range(len(self.classes))]
        self.net = cv.dnn.readNet(model_path)

        self.inp_sz = input_size
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold

    def postprocess(self, image_w, image_h, outs, ratio=None, pad=None):

        # ratioh, ratiow = image_h / 640, image_w / 640
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        nc = outs.shape[2] - 5
        # print('num cls:', nc)
        classIds = []
        confidences = []
        boxes = []

        conf_tmp = {i:[] for i in range(nc)}
        box_tmp = {i:[] for i in range(nc)}
        for batch in outs:
            # print(out.shape)
            for p, detection in enumerate(batch):

                scores = detection[5:] * detection[4]
                classId = np.argmax(scores, axis=0)
                confidence = scores[classId]

                if confidence > self.confThreshold:
                    center_x = detection[0]
                    center_y = detection[1]
                    width = detection[2]
                    height = detection[3]

                    left = ((center_x - width / 2) - pad[0]) / ratio[0]
                    top = ((center_y - height / 2) - pad[1]) / ratio[1]
                    width /= ratio[0]
                    height /= ratio[1]
                    # print(detection[:5])
                    conf_tmp[classId].append(float(detection[4]))
                    box_tmp[classId].append([int(left), int(top), int(width), int(height)])
        # print('box size: ', len(boxes))
        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.

        for i in range(nc):
            indices = cv.dnn.NMSBoxes(box_tmp[i], conf_tmp[i], self.confThreshold, self.nmsThreshold)

            if len(indices):
                indices = indices.flatten()
                boxes.append(np.array(box_tmp[i])[indices])
                confidences.append(np.array(conf_tmp[i])[indices])
                classIds += [i] * len(indices)
        if boxes:
            return np.concatenate(boxes), np.concatenate(confidences), np.array(classIds)
        else:
            return np.array(boxes), np.array(confidences), np.array(classIds)

    def __call__(self, srcimg):
        '''
        Args:
            srcimg:

        Returns:
            rect_boxes: a ndarray of [left, top, width, height]
            confidences: a ndarray of conf
            classIds: a ndarray of id
            dst: result image
        '''

        inp, r, d = letterbox(srcimg, new_shape=self.inp_sz, color=(114, 114, 114), auto=False, scaleFill=False)
        # print('r', r)
        # print('d', d)

        # blob = cv.dnn.blobFromImage(inp, 1 / 255.0, (640, 640), [0, 0, 0], swapRB=True, crop=False)
        inp = inp.astype(np.float32) / 255.

        blob = inp[:,:,::-1][np.newaxis,...].transpose(0, 3, 1, 2)
        # print('blob shape:', blob.shape)
        # print(blob[:,::,300, 300])
        # ims = cv.dnn.imagesFromBlob(blob)
        # cv.imshow('input', ims[0])
        # cv.waitKey()

        # Sets the input to the network
        # print(blob.shape)
        # self.net.setInputShape('images', (1, 3, 640, 640))
        self.net.setInput(blob)
        # print(self.net.getUnconnectedOutLayersNames())
        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.net.getUnconnectedOutLayersNames())[0]

        image_h, image_w = srcimg.shape[:2]

        img0_shape = srcimg.shape
        img1_shape = blob.shape[2:]
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
        # print('gain', gain)
        # print('pad', pad)
        rect_boxes, confidences, classIds = self.postprocess(image_w, image_h, outs, r, d)

        dst = srcimg.copy()
        for r, c, l in zip(rect_boxes, confidences, classIds):
            left, top, width, height = int(r[0]), int(r[1]), int(r[2]), int(r[3])
            # print((left, top, width, height))
            dst1 = (left, top, left + width, top + height)
            detect1 = (650, 515, 1550, 1100)
            iou = compute_IOU(dst1, detect1)
            print(iou)
            if iou >= 0.8:
                dst = cv.rectangle(srcimg, (left, top), (left + width, top + height), (0, 250, 0), 2)
                dst = cv.putText(dst, '%d: %.3f'%(l, c), (left, top-10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            else:
                dst = cv.rectangle(srcimg, (left, top), (left + width, top + height), (250, 250, 250), 2)

        return rect_boxes, confidences, classIds, dst

def compute_IOU(rec1,rec2):
    """
    计算两个矩形框的交并比。
    :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
    :param rec2: (x0,y0,x1,y1)
    :return: 交并比IOU.
    """
    left_column_max  = max(rec1[0],rec2[0])
    right_column_min = min(rec1[2],rec2[2])
    up_row_max       = max(rec1[1],rec2[1])
    down_row_min     = min(rec1[3],rec2[3])
    #两矩形无相交区域的情况
    if left_column_max>=right_column_min or down_row_min<=up_row_max:
        return 0
    # 两矩形有相交区域的情况
    else:
        S1 = (rec1[2]-rec1[0])*(rec1[3]-rec1[1])
        S2 = (rec2[2]-rec2[0])*(rec2[3]-rec2[1])
        S_cross = (down_row_min-up_row_max)*(right_column_min-left_column_max)
        return S_cross/(S1+S2-S_cross)


def vid_inf(video_path, yolov5):
    cap = cv.VideoCapture(video_path)

    while 1:
        ret, img = cap.read()
        boxes, confidences, classIds, dst = yolov5(img)
        cv.rectangle(dst, (650, 515), (1550, 1100), (0, 0, 255), 5)
        cv.namedWindow("dst", cv.WINDOW_FREERATIO)
        cv.imshow('dst', dst)

        if cv.waitKey(100) & 0xFF == ord('q'):
            break

def img_inf(image_path, yolov5):
    orig_image = cv.imread(image_path)
    t0 = time.time()
    boxes, confidences, classIds, dst = yolov5(orig_image)
    t1 = time.time()
    print('time use:', t1 - t0)
    cv.namedWindow("dst", cv.WINDOW_FREERATIO)
    cv.imshow('dst', dst)
    cv.waitKey(0)


img_suffix = ['.jpg', '.jpeg', '.png']
vid_suffix = ['.mp4', '.avi', '.flv', 'MP4']

img_path = '/home/myl/myl/biaozhu/gangjuan-1/30140.jpg'
vid_path = "/home/myl/myl/biaozhu/20220105/test1.MP4"

if __name__ == '__main__':
    classes = ['gangjuan']
    yolov5 = Yolov5(mode_path, classes, input_size=(320,320),
                    confThreshold=0.25,
                    nmsThreshold=0.45,
                    )
    # source_path = img_path
    source_path = vid_path

    suffix = osp.splitext(source_path)[-1].lower()
    if suffix in img_suffix:
        inf = img_inf
    elif suffix in vid_suffix:
        inf = vid_inf
    else:
        print('is not image or video')
        import sys

        sys.exit()

    inf(source_path, yolov5)
