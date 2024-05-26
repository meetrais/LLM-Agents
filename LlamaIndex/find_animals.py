import cv2
import image_analyzer as IA
import time

vidcap = cv2.VideoCapture('video/video4.mp4')
success,image = vidcap.read()
count = 0
while success:
  imagename = "frame%d.jpg" % count
  imagepath = 'images/data/'+imagename  
  cv2.imwrite(imagepath, image)     # save frame as JPEG file    
  time.sleep(4)
  IA.analyze(imagename)
  time.sleep(4)
  success,image = vidcap.read()
  count += 1
  if(count>9):
    success=False