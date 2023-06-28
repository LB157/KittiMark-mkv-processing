# mkv 转换为png  以时间戳命名
import cv2 as cv2
from datetime import datetime
import time
vidcap = cv2.VideoCapture('/home/liubo/Downloads/1219/20221219174105/20221219174105_video_01_Front.mkv')
img_path="/home/liubo/Downloads/1219/20221219174105/png/"
dt = "2022-12-19 17:41:05"
if vidcap.isOpened() is False:
    print("Error opening vieo stream or file")
success,image = vidcap.read()
count = 0
#转换成时间数组
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
#转换成时间戳
timestamp = time.mktime(timeArray)
local_time = timestamp 
while success:
  frame_index = vidcap.get(cv2.CAP_PROP_POS_MSEC) 
  #print('shijian:',frame_index)
  frame_time = frame_index/1000.0 + local_time
  cv2.imwrite(img_path+"%.6f.png" %frame_time, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  count += 1
