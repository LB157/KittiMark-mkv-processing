import cv2 as cv2
vidcap = cv2.VideoCapture('/home/liubo/Downloads/20221014143950_video_01_Front.mkv')
success,image = vidcap.read()
img_path="/home/liubo/Downloads/mkvpng/"
count = 0
while success:
  cv2.imwrite(img_path+"frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
