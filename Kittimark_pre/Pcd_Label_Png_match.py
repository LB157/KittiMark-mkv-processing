# 实现pcd、label、png文件以时间戳进行配对
# 相当与同一时间戳   以000000命名


import numpy as np
import cv2 as cv2
from datetime import datetime
import time
import os
import pclpy
import shutil
import glob

class FileMatch:
    def __init__(self, dir_path):
        file_dir = glob.glob(dir_path + "/*")
        self.filepath = []
        for f in file_dir:
            if f.endswith(".bag"):
                pass
            else:
                self.filepath.append(f)
 
    def match(self):
        for i in self.filepath:
            pcd_file = os.listdir(i + '/pcd')
            img_file = os.listdir(i + "/img")
            # label_file=os.listdir(+'/label')
            # print(img_file)
            for pcd in pcd_file:
                num=0
                print(i, pcd)
                pcd_prefix = os.path.splitext(pcd)[0]
                dict = {k:eval(pcd_prefix) - eval(os.path.splitext(k)[0]) for k in img_file}
                # dict_label = {kk:eval(pcd_prefix) - eval(os.path.splitext(kk)[0]) for kk in label_file}
                
 
                value = 0
                img_key, diff_val = min(dict.items(), key=lambda x: abs(value - x[1]))
                # label_key, labeldiff_val = min(dict_label.items(), key=lambda x: abs(value - x[1]))
                
                
                print(img_key, diff_val, pcd)
                # print(label_key, labeldiff_val, pcd)
                
                src_pcd=os.path.join(i,"pcd",pcd)
                new_pcd_path=i+"/pcd_new"
                if not os.path.exists(new_pcd_path):
                    os.makedirs(new_pcd_path)
                    
                # src_label=os.path.join(i,"label",label_key)
                # new_label_path=i+"/label_new"
                # if not os.path.exists(new_label_path):
                #     os.makedirs(new_label_path)
                
                src_img = os.path.join(i ,"img", img_key)
                new_img_path = i+"/img_new"
                if not os.path.exists(new_img_path):
                    os.makedirs(new_img_path)
                new_img = os.path.join(new_img_path, '{:06d}.png'.format(num))
                new_pcd= os.path.join(new_pcd_path, '{:06d}.pcd'.format(num))
                # new_label= os.path.join(new_pcd_path, '{:06d}.pcd'.format(num))
                # print(src_img)
                # print(new_img)
                shutil.copyfile(src_img, new_img)
                shutil.copyfile(src_pcd, new_pcd)
                num +=1
                





# root_dir="/home/liubo/Downloads/1219/20221219174105/20221219174105_video_01_Front.mkv"
file_dir="/home/liubo/Downloads/已标注_label格式/1(508)"

filematch=FileMatch(file_dir)
filematch.match()
# img_pathstring=root_dir.split("/") [-2]
# dt = "2023-02-07 15:57:02"
# timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
# #转换成时间戳
# timestamp = time.mktime(timeArray)
# local_time = timestamp 
# print(local_time)
# # print(img_savepath)
