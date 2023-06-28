# 实现pcd、label
#1.map  标准的垂直方位角 ，水平方位角
#2.强度非零的点 水平、垂直误差最小值 的map索引
#3.根据map索引生成128*1200 *2 矩阵       if  矩阵强度值为零 直接存    否则    比较强度值，最大的存   （强度值、原始数组索引）
#4.保存生成bin文件  
import math
import numpy as np
import cv2 as cv2
import yaml
from datetime import datetime
import time
import os
import pclpy
import shutil
import glob

class PointsMatch:
    def __init__(self, dir_path):
        file_dir = glob.glob(dir_path + "/*")
        self.filepath = []
        for f in file_dir:
            if f.endswith(".bag"):
                pass
            else:
                self.filepath.append(f)
 
    def get_h_map(self,yaml_name):
        try:
            print("Opening config file %s" %yaml_name )
            file=open(yaml_name, 'r')
            h_std = yaml.safe_load(file)
        except Exception as e:
            print(e)
            print("Error opening yaml file.")
            quit()
        h_dict = h_std["h"]
        file.close()   
        return h_dict
    def get_w_map(self):
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
        return arr
    def load_lidar_file(self,filename):
        """用pclpy读取pcd

        Args:
            filename (_type_): _description_
            n_features (int, optional): _description_. Defaults to 4.

        Returns:
            _type_: _description_
        """
        # if(filename.endswith(".bin")):
        #     point_clouds = np.fromfile(filename,dtype=np.float32).reshape(-1,4)
        #     print("bin 3 lens:",point_clouds[222222:222225,:])
        #     print("bin  shape:",point_clouds.shape)
            
        if(filename.endswith(".pcd")):
            pcd_reader = pclpy.pcl.io.PCDReader()
            pc = pclpy.pcl.PointCloud.PointXYZI()
            pcd_reader.read(filename, pc)
            xyz = pc.xyz
            intensity = pc.intensity.reshape(-1, 1)
            point_clouds = np.concatenate([xyz, intensity], axis=1)
            return point_clouds
        
    def pointshandle(self,points):
        intensity=points[:,3].reshape(len(points),1)
        test_points_xy=points[:,0:2]
        test_points_z=points[:,2]
        test_points_xoy=np.sqrt(np.sum(test_points_xy*test_points_xy,axis=1))
        h_angel_pi=np.arctan2(test_points_z,test_points_xoy)
        # print(np.arctan2(-3,math.sqrt(3)))
        h_angel=np.degrees(h_angel_pi).reshape(len(intensity),1)
        # print( np.degrees(np.arctan2(-3,math.sqrt(3))))
        print(h_angel)
        
        test_points_xz= points[:,[0,2]]
        test_points_y=points[:,1]
        test_points_xoz=np.sqrt(np.sum(test_points_xz*test_points_xz,axis=1))
        w_angel_pi=np.arctan2(test_points_y,test_points_xoz)
        w_angel=(np.degrees(w_angel_pi)).reshape(len(intensity),1)
        hwi_angel= np.concatenate((h_angel,w_angel, intensity),1)
        return hwi_angel
        # print(w_angel)
        
    def points_match(self,hwi_angel):
        dict = {k:eval() - eval}
# dict_label = {kk:eval(pcd_prefix) - eval(os.path.splitext(kk)[0]) for kk in label_file}
        value = 0
        # 检查水平角、垂直角、强度误差最小值的索引是否一样
        #全是零的数据如何剔除
        img_key, diff_val = min(dict.items(), key=lambda x: abs(value - x[1]))
        
        
        
        
        
    def match(self):
        for i in self.filepath:
            pcdpath=os.path.join(i,'pcd')
            # pcd_file = os.listdir(pcdpath)
            file_dir = glob.glob(pcdpath + "/*")
            pcd_file = []  
            for f in file_dir:
                if f.endswith(".DS_Store"):
                    pass
                else:
                    pcd_file.append(f)
                    
            h_name=self.get_h_map('h_map.yaml')
            w_stdmap=self.get_w_map()
            for pcdfile in pcd_file:
                pcdpoints=self.load_lidar_file(pcdfile)
                hwi_points=self.pointshandle(pcdpoints)
                hwi_arr_points=np.zeros((128,1200,2))
                for point_num in range(hwi_points.shape[0]):
                    if hwi_points[point_num,2]!=0:
                        h_diff={k:abs(h_name[k]-hwi_points[point_num,0])  for k in h_name.keys()}
                        h_true_key,h_true_value=min(h_diff.items(), key=lambda x: abs(x[1]))
                # for h_key,h_value in h_name.items():
                #     if h_value==12.73:
                #         key=h_key
                #         break
                        w_map=w_stdmap[h_true_key,:]
                        w_diff={k:abs(w_map[k]-hwi_points[point_num,1])  for k in range(w_map.size)}
                        w_true_key,w_true_value=min(w_diff.items(),key=lambda x: abs(x[1]))
                        #强度值和序列号
                        if hwi_arr_points[h_true_key,w_true_key,0]<hwi_points[point_num,2]:
                            hwi_arr_points[h_true_key,w_true_key,0]=hwi_points[point_num,2]
                            hwi_arr_points[h_true_key,w_true_key,1]=point_num
                print('save_pcd_part:hwi_arr_points')
                # md_points=np.zeros((153600,4))
                hh=hwi_arr_points[:,:,1].reshape(-1)
                # md_points[0:len(hh),:]=pcdpoints[hh,:]
                md_points=pcdpoints[hh.astype('int64'),:]
                print()
                
                
            break
            print()
                
                
                

            
    # def save_pcd():
    #     new_pcd_path=i+"/pcd_new"





# root_dir="/home/liubo/Downloads/1219/20221219174105/20221219174105_video_01_Front.mkv"
# file_dir="/home/liubo/Downloads/已标注_label格式/1(508)"


file_dir="/home/liubo/Downloads/dataimport/output"

filematch=PointsMatch(file_dir)

filematch.match()
# img_pathstring=root_dir.split("/") [-2]
# dt = "2023-02-07 15:57:02"
# timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
# #转换成时间戳
# timestamp = time.mktime(timeArray)
# local_time = timestamp 
# print(local_time)
# # print(img_savepath)
