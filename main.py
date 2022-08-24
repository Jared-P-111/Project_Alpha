import cv2 as cv
import numpy as np
import keyboard
import math
from time import time
from Screen_capture import ScreenCapture
from SIFT_BF_feature_match import SIFT_Brute_Feature_Match
from m_and_k_tracking import MouseAndKeyTracking
from template_match import TemplateMatch
from Flann_feature_match import FeatureMatchFlann



#CREATE INSTANCES OF SCREEN CAPTURE & template_match
screenCap = ScreenCapture(0, 2)
print("Screen Capture ready. Press s to continue.")

#INSTANCE SUITE (Select type) add Import
template_match = TemplateMatch('./images/needle.JPG')
flann_feature_match = FeatureMatchFlann("./images/needle.JPG")
sift_feature_match = SIFT_Brute_Feature_Match("./images/needle.JPG")

#DISPLAY SCREENS INFO
screenCap.camInfo()

#START CAMERA
keyboard.wait("s")
screenCap.camera_start(60, 0, 0, 1920, 1080)
print("Camera running ready for screen capture press s to start.")
print("focus window and press q to quit.")

#TIME STAMP
loop_time = time()

#START LOOP FOR SCREEN CAPTURE AND CONVERSION TO CV FILE
while(True):
  #READ OUT DETECTED POINTS
  screenshot = screenCap.currCamera.get_latest_frame()
  screenshot = np.array(screenshot)
  screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
  
  imageData = sift_feature_match.findNeedle(screenshot)

  cv.imshow('Found Needle', imageData["image"])

  #TIME TRACKING FOR FPS
  stamp = math.floor(1 / (time() - loop_time))
  print('FPS: {}'.format(stamp))
  loop_time = time()

  #SHUTDOWN PROGRAM
  if cv.waitKey(1) == ord('q'):
    cv.destroyAllWindows()
    break

print('Done.')
