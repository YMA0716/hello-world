import xml.etree.ElementTree as ET
import os
import random
import glob
import shutil

data_dir = '/home/myl/myl/biaozhu/voc2007'
yolo_dir = '/home/myl/myl/biaozhu/yolo2022'

classes = ["gangjuan"]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(voc_file, target_dir):
    in_file = open(voc_file)
    image_id = os.path.splitext(os.path.basename(voc_file))[0]
    out_file = open('%s/%s.txt'%(target_dir, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def main(train_txt=None, val_txt=None):
    # generate dir
    os.makedirs(os.path.join(yolo_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(yolo_dir, 'labels', 'val'), exist_ok=True)
    os.makedirs(os.path.join(yolo_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(yolo_dir, 'images', 'val'), exist_ok=True)

    imgs = glob.glob(data_dir + '/JPEGImages/*.jpg')
    if train_txt is None and val_txt is None:
        num_slection = int(len(imgs) * 0.7)
        train_list = random.sample(imgs, num_slection)
    else:
        train_list = [os.path.join(data_dir + '/JPEGImages/', name + '.jpg')
                      for name in open(train_txt, 'r')]
        val_list = [os.path.join(data_dir + '/JPEGImages/', name + '.jpg')
                    for name in open(val_txt, 'r')]
    for img_path in imgs:
        if img_path in train_list:
            target_img_path = os.path.join(yolo_dir, 'images', 'train')
            target_txt_dir =  os.path.join(yolo_dir, 'labels', 'train')
        else:
            target_img_path = os.path.join(yolo_dir, 'images', 'val')
            target_txt_dir =  os.path.join(yolo_dir, 'labels', 'val')

        if (os.path.exists(img_path)):
            xml_path = img_path.replace('JPEGImages', 'Annotations').replace('.jpg', '.xml')
            convert_annotation(xml_path, target_txt_dir)
            shutil.copy(img_path, target_img_path)

if __name__ == '__main__':
    main()