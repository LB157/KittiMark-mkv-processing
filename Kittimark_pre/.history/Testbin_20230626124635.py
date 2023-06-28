# 实现pcd bin label文件加载
# 实现mkv转png，以时间戳命名


import numpy as np

import cv2 as cv2
from datetime import datetime
import time
import os
import pclpy

class  Semantickittifileset(object):
    def __init__(self,data_dir) -> None:
        self.data_dir=data_dir    #需要处理的数据单个文件目录
        self.lidar_dir=os.path.join(self.data_dir,"velodyne")
        # files=os.listdir(self.lidar_dir)
        # self.num=len(files)
        
    # def __len__(self) :
        # return self.num
    
    def read_label(self,filename):
        if(filename.endswith(".label")):
            frame_labels=np.fromfile(filename,dtype=np.int32)
            sem_labels =frame_labels & 0xFFFF
            print("label value(max.min):",sem_labels.max(),sem_labels.min())
            print("label  shape:",sem_labels.shape)
            
            
    def load_lidar_file(self,filename,features=4):
        """用pclpy读取pcd

        Args:
            filename (_type_): _description_
            n_features (int, optional): _description_. Defaults to 4.

        Returns:
            _type_: _description_
        """
        if(filename.endswith(".bin")):
            point_clouds = np.fromfile(filename,dtype=np.float32).reshape(-1,4)
            print("bin 3 lens:",point_clouds[222222:222225,:])
            print("bin  shape:",point_clouds.shape)
            
        if(filename.endswith(".pcd")):
            if(features == 4):
                pcd_reader = pclpy.pcl.io.PCDReader()
                pc = pclpy.pcl.PointCloud.PointXYZI()
                pcd_reader.read(filename, pc)
                xyz = pc.xyz
                intensity = pc.intensity.reshape(-1, 1)
                point_clouds = np.concatenate([xyz, intensity], axis=1)
                print("pcd 3 lens:",point_clouds[222222:222225,:]) 
                print("pcd shape:",point_clouds.shape)

    def  mkv2png(self,filename):
            img_save=os.path.abspath(os.path.join(filename,"../.."))
            img_savepath=os.path.join(img_save,'img','')
            filenm=filename.split("/")[-1]
            timeArry =time.strptime( filenm.split("_")[-4],"%Y%m%d%H%M%S")
            print(timeArry)
            vidcap = cv2.VideoCapture(filename)
            if vidcap.isOpened() is False:
                print("Error opening vieo stream or file")
            success,image = vidcap.read()
            count = 0
            #转换成时间数组
            #转换成时间戳
            timestamp = time.mktime(timeArry)
            local_time = timestamp 
            while success:
                frame_index = vidcap.get(cv2.CAP_PROP_POS_MSEC) 
                #print('shijian:',frame_index)
                frame_time = frame_index/1000.0 + local_time
                cv2.imwrite(img_savepath+"%.6f.png" %frame_time, image)     # save frame as JPEG file      
                success,image = vidcap.read()
                count += 1
            
    def get_lidar(filename):
        data=np.load(filename)
        print("npyl:",data.shape)
        print("npyl:",data[41,1000:1003,:])
        
        
            

if __name__ == '__main__':
# label
    root_dir="/home/liubo/Downloads/AT128_remark_label/20230130/pcd_1185/20230130/20230131162446/"
    # root_dir="/home/liubo/Downloads/4号-20230131162446(2)/dev/shm/1684739465443479_222bf492-f534-402f-92de-2fdb8397e2f6/1646316521876996097/4号-20230131162446/20230131162946"
    
    kittifileset=Semantickittifileset(root_dir)
    # label_dir=os.path.join(root_dir,'2(368)','20230131164231','label')
    # print("dizhi:",label_dir)
    # for vf in os.listdir(label_dir) :
    #     if vf.endswith('.label'):
    #         filename=os.path.join(label_dir,vf)
    #         kittifileset.read_label(filename)
    # load_lidar_file( "/home/liubo/Downloads/2号/20230131164103/1675154515.530591.bin")
    # load_lidar_file( "/home/liubo/Downloads/1675154515.530591.label")
    # get_lidar('/home/liubo/Downloads/at128data/renpy/000145.npy')
    
    # mkv to png
    file_dir=os.path.join(root_dir,'srcpcd')
    for vf in os.listdir(file_dir):
        name_src=os.path.splitext(vf)[0]
        pcd_name=os.path.join(file_dir,vf)
        label_name=os.path.join(root_dir,'label', name_src+'.label')
        # bin_name=os.path.join(root_dir,'bin',name_src+'.bin')
        kittifileset.load_lidar_file(pcd_name)
        # kittifileset.load_lidar_file(bin_name)
        kittifileset.read_label(label_name)
        
             
        
    
    
    

 