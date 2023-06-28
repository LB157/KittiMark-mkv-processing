# 测试pcd转为bin
# 


import numpy as np
import yaml
import cv2 as cv2
import time
import os
import pclpy

yamlpath='hwmap.yaml'
hw=np.array([[[0,2],[1,4]],[[2,6],[3,8]],[[4,10],[4,12]]])
print(hw.shape)
hh=np.zeros((100,2))
ha=np.array([[1,2],[3,4],[5,6],[7,8],[9,10]])
hb=hw[:,:,0].reshape(-1)
hh[0:len(hb),:]=ha[hb,:]
data={"date":123,
      "date2":{"k1":1
          }}
dict=dict()
dict={i:hw[i,0]  for i in range(hw.shape[0])}
print(dict)
with open(yamlpath,"w",encoding="utf-8") as f:
    yaml.dump(dict,f,encoding='utf-8',default_flow_style=False,allow_unicode=True)