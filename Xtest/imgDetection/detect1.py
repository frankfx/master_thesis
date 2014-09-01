'''
Created on Aug 29, 2014

@author: rene
'''
import numpy as np
import cv2

img = cv2.imread('wing.jpg')
gray = cv2.imread('wing.jpg',0)

ret,thresh = cv2.threshold(gray,127,255,1)

contours,h = cv2.findContours(thresh,1,2)
n = 0

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print "Rene" , len(approx)
    if len(approx)==5:
        print "pentagon"
        print cnt
        cv2.drawContours(img,[cnt],0,255,0)
    n+=1
    if n == 2 :
      break
    
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()