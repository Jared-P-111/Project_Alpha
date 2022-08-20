import cv2 as cv
import numpy as np


class TemplateMatch: 

    #properties
    needle_img = None
    curr_needle_w = 0
    curr_needle_h = 0
    method = None
    
    #Constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):

        #Use Match Template on image
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        #Get size of needle img for rectangle size
        self.curr_needle_w = self.needle_img.shape[1]
        self.curr_needle_h = self.needle_img.shape[0]

        #current selected OpenCV Match Template Method
        self.method = method

    def findNeedle(self, haystack_img, threshold, debug_mode = None):

        
        #Stored data after calculating matches
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)
        
        #Loops through all points of result and returns only ones higher then threshold in a matrix
        locations = np.where(result >= threshold)

        #converts the returned matrix into an X, Y list (for info look up list, zip, *)
        locations = list(zip(*locations[::-1]))
        

        #Group Rectangles removes duplicated rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.curr_needle_w, self.curr_needle_h]
            rectangles.append(rect)
    
        rectangles = cv.groupRectangles(rectangles, 1, 0.7)[0]

        data = {"image": haystack_img, "points": []}
        if len(rectangles):
            #Set variables for the box on screen
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            #Loop over all the locations and draw rectangle on matches 
            for (x, y, w, h) in rectangles: #<-- Destructuring from rectangles [[x, y, w, h], ...]
    
                #Find center of each rectangle
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                #Save all the points in list
                data["points"].append((center_x, center_y))

                
                #Determine the box positions
                top_left = (x, y)
                bottom_right = (x + w, y + h)

                #Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, line_color)
                data["image"] = haystack_img 
        
        else:
            return data
            
        return data

        