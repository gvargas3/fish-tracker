# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:57:13 2019

@author: Brent Wickenheiser
contact: brentmw1@gmail.com
"""

import cv2
import numpy as np
import matplotlib.pyplot as pl
import csv
#
def trackVideo(filePath, imagePath, resultPath, dividerLine=0.5): 
    video = cv2.VideoCapture(filePath)
    image = cv2.imread(imagePath)
    #image2 = cv2.imread('brown.jpg')
    _, startFrame = video.read()
    
    #info for tracking time
    frameRate = video.get(cv2.CAP_PROP_FPS)
    
    #Length and width of video
    yMax = np.shape(startFrame)[0]
    dividerLine = np.round(dividerLine * yMax)
    xMax = np.shape(startFrame)[1]
    
    boxWidth = (xMax / 5)
    boxHeight = (yMax / 4)
    
    roi1 = image

    hsv_roi = cv2.cvtColor(roi1,cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi],[0], None, [180], [0,180])
    roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    showFrames = True
    start = True
    closeWindows = False
    allPoints = 0
    frameCount = 0
    wait = 85
    
    #Loops through all frames of video, using meanshift to update tracking window
    while True:
        ret, frame = video.read()
        if ret == True:
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask = cv2.calcBackProject([hsv], [0], roi_hist, [0,180],1)
           
            if (start):
                try:
                    _, track_window = cv2.meanShift(mask, (int(np.round(np.mean(np.where(mask == np.max(mask))[1]))) - int(boxWidth), int(np.round(np.mean(np.where(mask == np.max(mask))[0]))) - int(boxHeight),int(boxWidth*2),int(boxHeight*2)), term_criteria)
                    #_, track_window = cv2.meanShift(mask, (int(np.round(np.mean(np.where(mask == 1)[1]))) - 60, int(np.round(np.mean(np.where(mask == 1)[0]))) - 40,120,80), term_criteria)
                except:
                    frameCount = frameCount + 1
                    continue
            else:
                _, track_window = cv2.meanShift(mask, track_window, term_criteria)
                    
            x,y,w,h = track_window
            cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
            cv2.rectangle(mask, (x,y), (x+w,y+h),(0,255,0),2)
            trackRange = mask[y:y+h+1,x:x+w+1]
            try:
                pointX = int(x + np.round(np.mean(np.where(trackRange == np.max(trackRange))[1])))
                pointY = int(y + np.round(np.mean(np.where(trackRange == np.max(trackRange))[0])))
            except:
                pointX = int(x + w/2)
                pointY = int(y + h/2)
            cv2.circle(frame, (pointX, pointY), 2, 255)
            cv2.circle(mask, (pointX, pointY), 2, 255)
            
            #pointX = int(np.round(np.mean(np.where(mask == 1)[1])))
            cv2.circle(frame, (int(x + w/2), int(y + h/2)),2, 255)
            frameCount = frameCount + 1
            timeStamp = np.round(1000*frameCount/frameRate)
            
            #point = np.array([[timeStamp,int(x + w/2),int(y + h/2)]])  
            point = np.array([[timeStamp, pointX, pointY]])
            if start:
                allPoints = point
                start = False
            else:           
                allPoints = np.concatenate((allPoints, point), axis = 0)

            if showFrames:
                cv2.imshow("mask", mask)
                cv2.imshow("frame",frame)
            if closeWindows:
                cv2.destroyAllWindows()
                closeWindows = False
                wait = 0
            key = cv2.waitKey(wait)
            if key == 27:
                showFrames = False  
                closeWindows = True

        else:
            break
        
    # controls the level of smoothing
    level = 3
    smoothRange = range(-level, level+1)
    
    #For smoothing fish position
    end = np.shape(allPoints)[0] - level
    i = level+1
    allPoints[:,2] = yMax - allPoints[:,2]  # flip 
    dividerLine = yMax - dividerLine
    while i < end:
        xSum = 0
        ySum = 0
        for n in smoothRange:
            xSum = xSum + allPoints[i+n][1]
            ySum = ySum + allPoints[i+n][2]
        tot = len(smoothRange)
        allPoints[i][1] = np.round(xSum / tot) # average
        allPoints[i][2] = np.round(ySum / tot)

        i = i + 1
    
    #Writes points to csv file
    with open(resultPath + '.csv','w',newline='') as f:
        out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        #output = csv.DictWriter(f,delimiter=',', fieldnames=allPoints)
        midPoint = [1000,dividerLine,0]
        out.writerow(midPoint)
        for rows in allPoints:
            out.writerow(rows)    
    video.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    
    return
#"C:\Users\Brent\Desktop\fish-tracker\Python\tests\newestTest\newestTest.mp4"
# did Python/ because I am working in the git repo's root directory
#trackVideo("Python/tests/newestTest/newestTest.mp4", "Python/folder.png", "Python/newTest")
#trackVideo(".\\tests\\TEST2\\TEST2.mp4","brown.jpg",".\\tests\\TEST2\\TEST2")
#trackVideo("testVid.mp4","brown.jpg","testes")