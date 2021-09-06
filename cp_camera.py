#调用电脑摄像头录制一段视频
import  cv2
import  numpy as np
from datetime import  datetime

filename = 'myVideo.MP4'
width = 1280
height = 720
fps = 24.0
time = 10 # 计划录制视频的时长，单位为秒

#必须指定cv2.CAP_DSHOW(Direct Show)参数初始化摄像头，否则无法使用更高分辨率
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#设置摄像头分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#设置摄像头帧率，默认值为600
cap.set(cv2.CAP_PROP_FPS,fps)
#设置编码类型
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(filename,fourcc,fps,(width,height))
start_time = datetime.now()
while True:
    ret,frame = cap.read()
    if ret:
        out.write(frame)
        #显示预览窗口
        cv2.imshow("capture",frame)
    #10秒之后停止
    if (datetime.now() -start_time).seconds == time:
        cap.release()
        break
    #按下ESC后停止录制
    if  cv2.waitKey(3) & 0xff == 27:
        cap.release()
        break

out.release()
cv2.destroyAllWindows()