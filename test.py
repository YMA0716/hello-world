import cv2


# 图片的读取与写入

imgdir = '/home/myl/myl/workspace/photo/test01'  # 绝对路径
imgsave = '/home/myl/myl/workspace/photo/newtest01.png'
img = cv2.imread(imgdir)  # 读取

# 像素值的获取
pixel = img.item(100, 100, 2)
print(pixel)

# 图片性质
print(img.shape)  # 返回（882,700,3） 宽，长，3通道
print(img.size)
print(img.dtype)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img_threshold = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("img", img)
cv2.imshow("thRe", img_threshold)
key = cv2.waitKey(0)
if key == 27:
    print(key)
    cv2.destroyAllWindows()
cv2.imwrite(imgsave, img_threshold)  # 写入

# ROI 截取
roi = img[100:200, 300:400]
img[50:150, 200:300] = roi
b = img[:, :, 0]
b, g, r = cv2.split(img)
img = cv2.merge((b, g, r))
print(img)
#