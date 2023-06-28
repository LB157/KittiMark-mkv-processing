import cv2 as cv2
from datetime import datetime
import time
vidcap = cv2.VideoCapture('/home/liubo/personal/project/AT128/20221014143950_video_01_Front.mkv')
if vidcap.isOpened() is False:
    print("Error opening vieo stream or file")
local_str_time = datetime.fromtimestamp(1664505571.335263).strftime('%Y-%m-%d %H:%M:%S.%f') 
print('时间：',local_str_time)
success,image = vidcap.read()
#img_path="/home/liubo/Downloads/mkvpng/png/"
count = 0
while count:
  #cv2.imwrite(img_path+"frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  frame_index = vidcap.get(cv2.CAP_PROP_POS_MSEC) 
  print('Read a new frame time: ', frame_index)
  count += 1
