import dxcam
from time import time

class ScreenCapture:

  #INSTANTIATE THE CURRCAMERA
  currCamera = dxcam.create(output_color="RGB")


  #CONSTRUCTOR
  def __init__(self, device_idx = 0, output_idx = 0):

    #INTRODUCE CONSTRUCTOR PARAMS
    self.currCamera = dxcam.create(device_idx=device_idx, output_idx=output_idx)

  
  def camInfo(self):
    #OUTPUT INFO FOR CURRENT USER
    info = dxcam.output_info()
    print(info)

  #START CAMERA METHOD
  def camera_start(self, fps, locA, locB, width, height):   
    self.currCamera.start(target_fps=fps, region=(locA, locB, width, height))