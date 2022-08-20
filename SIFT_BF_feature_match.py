import cv2 as cv

class SIFT_Brute_Feature_Match:

  def __init__(self, needle_img_path):
    self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

  def findNeedle(self, haystack_img, threshold=None):

    #Create an SIFT object for detection
    siftObj = cv.SIFT_create()

    #Detect using siftObj detection
    kp1, des1 = siftObj.detectAndCompute(self.needle_img, None, )
    kp2, des2 = siftObj.detectAndCompute(haystack_img, None, )

    #Use Brute Force matching. 
    bf = cv.BFMatcher()

    matches = bf.knnMatch(des1, des2, k=2)

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
      # print(bestMatchObj.distance)

      #Extract coords 
      (x1, y1) = kp2[bestObjKeyPoint].pt

      #Marker Settings
      marker_type = cv.MARKER_STAR
      marker_color = (255, 0, 0)

      #Draw on screen.
      image = cv.drawMarker(haystack_img, (int(x1), int(y1)), marker_color, markerType=marker_type, markerSize=200, thickness=2)

      #update image
      data[0] = image

    except:
      print("No trainIdx found...")

    return data
