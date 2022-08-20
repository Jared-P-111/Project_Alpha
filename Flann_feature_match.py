import cv2 as cv

class FeatureMatchFlann:

  #properties
  needle_img = None
  curr_needle_w = 0
  curr_needle_h = 0

  def __init__(self, needle_img_path):
    self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

    #Get size of needle img for rectangle size
    self.curr_needle_w = self.needle_img.shape[1]
    self.curr_needle_h = self.needle_img.shape[0]

  def findNeedle(self, haystack_img, threshold=None):
    #Create a sift object (Scale & Variant Feature Transform)
    sift = cv.SIFT_create()

    #Detect using Sift and FLann
    kp1, des1 = sift.detectAndCompute(self.needle_img, None)
    kp2, des2 = sift.detectAndCompute(haystack_img, None)

    #FLANN
    FLANN_INDEX_TREE = 0
    index_params = dict(algorithm=FLANN_INDEX_TREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k = 2) 

    #Find lowest distance score
    bestMatch = matches[0][0].distance - matches[0][1].distance 
    
    #Store best Object 
    bestMatchObj = matches[0]  

    #Loop through Tuple to find best Match
    for match1, match2 in matches:

      #Subtract distances to find lowest distance score
      currNum = match1.distance - match2.distance

      if(currNum < bestMatch):
        bestMatch = currNum
        bestMatchObj = match1

    data = {"image": haystack_img, "points": []}

    try:
      bestObjKeyPoint = bestMatchObj.trainIdx
      print(bestMatchObj.distance)
      #Extract coords 
      (x1, y1) = kp2[bestObjKeyPoint].pt

      #Marker Settings
      marker_type = cv.MARKER_CROSS
      marker_color = (255, 0, 0)

      #Draw Marker on screen.
      image = cv.drawMarker(haystack_img, (int(x1), int(y1)), marker_color, markerType=marker_type, markerSize=200, thickness=2)

      #update image
      data[0] = haystack_img

    except:
      print("No trainIdx found...")

    return data

  
