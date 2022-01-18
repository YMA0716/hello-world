import os 
import argparse
import numpy as np
import lxml.builder
import lxml.etree

root = '/home/myl/myl/biaozhu/test/'
# for file in os.listdir(xmlPath):
#     pass
#
#
# parser = argparse.ArgumentParser()
# parser.add_argument('root')
# args = parser.parse_args()
# root = args.root
# print(root)

#noneed = 'hxq'
needs = ['gangjuan']
upper_root = os.path.abspath(os.path.join(root, '..'))
base_folder = os.path.basename(root)

ori_xml = os.path.join(root, 'xml') #'Annotations')
ori_img = os.path.join(root, 'img') #'JPEGImages')

des_path = os.path.join(root, 'VOC2007')
des_xml = os.path.join(des_path,'Annotations')
des_img = os.path.join(des_path,'JPEGImages')
if not os.path.exists(des_path):
    os.mkdir(des_path)
    os.mkdir(des_xml)
    os.mkdir(des_img)

files = os.listdir(ori_xml)

for fi in files:
    base = os.path.splitext(fi)[0]
    print(os.path.join(ori_xml, fi))
    old = lxml.etree.parse(os.path.join(ori_xml, fi))

    objs = old.findall('object')
    labels = [obj.find('name').text for obj in objs]

    # for noneed labels
    #if list(set(labels)) == [noneed]:
    #    continue

    # for need labels
    label_flag = False
    for need in needs:
        if need in labels:
            label_flag = True
            break
    if label_flag == False:
        continue

    maker = lxml.builder.ElementMaker()
    xml = maker.annotation(
            maker.folder('VOC2007'),
            maker.filename(base+".jpg"),
            maker.database(),
            maker.annotation(),
            maker.image(),
            maker.size(
                maker.height(old.find('size').find('height').text),
                maker.width(old.find('size').find('width').text),
                maker.depth(old.find('size').find('depth').text),
                ),
            maker.segmented(),
            )

    for obj in objs:
        #if obj.find('name').text != noneed:
        for need in needs:
            if obj.find('name').text == need:
                BndBox = obj.find('bndbox')
                xml.append(
                    maker.object(
                        maker.name(obj.find('name').text),
                        maker.pose('Unspecified'),
                        maker.truncated('0'),
                        maker.difficult('0'),
                        maker.bndbox(
                            maker.xmin(BndBox.find('xmin').text),
                            maker.ymin(BndBox.find('ymin').text),
                            maker.xmax(BndBox.find('xmax').text),
                            maker.ymax(BndBox.find('ymax').text),
                            ),
                        )
                    )

    os.system('cp ' + os.path.join(ori_img, base+'.jpg') + ' ' + des_img)
    with open(os.path.join(des_xml, fi), 'wb') as f:
        f.write(lxml.etree.tostring(xml, pretty_print=True))
