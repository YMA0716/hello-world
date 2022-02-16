import os
import shutil
import csv
import pandas as pd

# csvFile = '/home/myl/data/csv/'
# imgPath = '/home/myl/data/ori/'
# fileImg = '/home/myl/data/'
csvFile = '/home/myl/data/lcc/topk_ids.csv'
target_img = '/home/myl/myl/biaozhu/lcc_photo_2/'
res_img = '/home/myl/data/lcc/'

# for file in os.listdir(csvFile):
#     ll = file.split('.')[0].split('_')
#     newll = ll[2]+'_'+ll[3]
f = csv.reader(open(csvFile, 'r'))
for i in f:
    # print(i)
    print(target_img + i[0])
    # print(type(i[1]))
    if i[1] == '0':
            shutil.copy(target_img + i[0], res_img + '0/')
    else:
            shutil.copy(target_img + i[0], res_img + '1/')
'''
pandas
'''
# def pandas_classify(csvFile):
#     for file in os.listdir(csvFile):
#         df = pd.read_csv(csvFile + file)
#         print(type(df))
#         print(df.to_string())


'''
csv
'''

# def classify(csvFile):
#     for file in os.listdir(csvFile):
#         ll = file.split('.')[0].split('_')
#         newll = ll[2]+'_'+ll[3]
#         os.mkdir(fileImg + newll + "/0/")
#         os.mkdir(fileImg + newll + "/1/")
#         f = csv.reader(open(csvFile + file, 'r'))
#         for i in f:
#             # print(i)
#             # print(imgPath + newll + '/' + i[0])
#             # print(type(i[1]))
#             if i[1] == '0':
#                 shutil.copy(imgPath + newll + '/' + i[0], fileImg + newll + '/0/')
#             else:
#                 shutil.copy(imgPath + newll + '/' + i[0], fileImg + newll + '/1/')
#
#
# if __name__ == '__main__':
#      classify(csvFile)
