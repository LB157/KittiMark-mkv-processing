#单帧图片去除畸变
import numpy as np
import os
import sys
import cv2
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_file=os.path.join(BASE_DIR, 'png','1666686695.000000.png')
camera_intrinsic_matrix=np.array( [[959.7880859375,0,1027.951416015625],
      [0,960.2677001953125,512.572998046875],
      [0,0,1]])
camera_distortion=np.array([-0.542839716456304,0.319373567687993,0,0,-0.132538841670150])
img_data=cv2.imread(file_file)
img_dst = cv2.undistort(img_data, camera_intrinsic_matrix, camera_distortion)
# self.scan_infer_vis5000.set_data(self.scan.points5000,#points5000为xyz点的坐标
#                                  face_color=viridis_colors[..., ::-1],  # self.scan.pre_label_color
#                                  edge_color=viridis_colors[..., ::-1],
#                                  siz
newfile_path=os.path.join(BASE_DIR, 'newpng','0.png')
cv2.imwrite(newfile_path,img_dst)


