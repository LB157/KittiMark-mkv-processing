# 双回波变为单回波 模块之一
# 128*1200 标准映射表


import numpy as np
import yaml
import cv2 as cv2
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
            
            print("bin  shape:",point_clouds.shape)
            
        if(filename.endswith(".pcd")):
            if(features == 4):
                pcd_reader = pclpy.pcl.io.PCDReader()
                pc = pclpy.pcl.PointCloud.PointXYZI()
                pcd_reader.read(filename, pc)
                xyz = pc.xyz
                intensity = pc.intensity.reshape(-1, 1)
                point_clouds = np.concatenate([xyz, intensity], axis=1)
                return point_clouds

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
                
                
    def save_bin(self,pointsnpy):
        pointsnpy.tofile('1.bin')
        
    def save_yaml(self):
        flag=True
        arr=np.empty((128,1200))
        for i in range(128):
            if (flag==True):
                if (i+1%2!=0):
                    arr[i,0]=60-2.16
                else:
                     arr[i,0]=60+0.56
            if (flag==False):
                if (i+1%2!=0):
                    arr[i,0]=60+2.16
                else:
                     arr[i,0]=60-0.56
                
            if i+1%16==0:
                flag=not(flag)
            for j in range(1,1200):
                arr[i,j]=arr[i,j-1]-0.1
        for i in range(128):
            dicta={j:float(arr[i,j]) for j in range(arr.shape[1])}     
            dictb={i:dicta}  
            with open("hw_std.yaml",'a',encoding='utf_8') as f: 
                yaml.dump(dictb,f,encoding='utf_8',allow_unicode=True)
        h_arr={}
        h_arr[0]=12.93
        for m in range(1,128):
            h_arr[m]=h_arr[m-1]-0.2
        dicth={l:h_arr[l] for l in range(128)}
        dicthh=dict(h=dicth)
        with open("h_map.yaml",'a',encoding='utf_8') as f: 
            yaml.dump(dicthh,f,encoding='utf_8',allow_unicode=True)
        

if __name__ == '__main__':
# label
    # root_dir="/home/liubo/Downloads/4号-20230131162446(2)/dev/shm/1684739465443479_222bf492-f534-402f-92de-2fdb8397e2f6/1646316521876996097/4号-20230131162446/pcd"
    # root_dir="/home/liubo/Downloads/4号-20230131162446(2)/dev/shm/1684739465443479_222bf492-f534-402f-92de-2fdb8397e2f6/1646316521876996097/4号-20230131162446/20230131162946"
    root_dir="/home/liubo/Downloads/4号-20230131162446(2)/dev/shm/1684739465443479_222bf492-f534-402f-92de-2fdb8397e2f6/1646316521876996097/4号-20230131162446/pcd/pcd/1675153734.988864.pcd"
    
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
    points=kittifileset.load_lidar_file(root_dir)
    kittifileset.save_bin(points)
    kittifileset.load_lidar_file('1.bin')
    kittifileset.save_yaml()
        
    
    
    

 