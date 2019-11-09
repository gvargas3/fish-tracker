# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:57:13 2019

@author: Brent
"""

import cv2
import numpy as np


video = cv2.VideoCapture("testVid.mp4")
image = cv2.imread("brown.jpg")

#ret,frame = cap.read()

_, frame1 = video.read()
x = 560
y = 225
width = 20
height = 38
roi = frame1[y:y+height,x:x+width]
roi1 = image

#cv2.imshow('roi',roi)
cv2.waitKey(0)
hsv_roi = cv2.cvtColor(roi1,cv2.COLOR_BGR2HSV)

roi_hist = cv2.calcHist([hsv_roi],[0], None, [180], [0,180])
roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
frameNum = 0
while True:
    _, frame = video.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.calcBackProject([hsv], [0], roi_hist, [0,180],1)
    #print(int(np.floor(np.mean(np.where(mask == 1)[0]))))
    #print(int(np.floor(np.mean(np.where(mask == 1)[1]))))
    #print(mask.shape())
    if (frameNum == 0):
        print(0)
        _, track_window = cv2.meanShift(mask, (int(np.floor(np.mean(np.where(mask == 1)[1]))) - 60, int(np.floor(np.mean(np.where(mask == 1)[0]))) - 40,120,80), term_criteria)
    else:
        _, track_window = cv2.meanShift(mask, (x,y,125,75), term_criteria)
    _, track_window = cv2.meanShift(mask, (x,y,125,75), term_criteria)
    x,y,w,h = track_window
    cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
    print(track_window)
    #cv2.imshow("mask", mask)
    frameNum = frameNum + 1
    cv2.imshow("frame",frame)
    
    key = cv2.waitKey(60)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()
