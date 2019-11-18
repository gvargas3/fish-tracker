# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:27:13 2019

@author: Brent
"""
import matplotlib.pyplot as pl
import fileManipulation as fm
import numpy as np
import os

def endPoints(fileName, middle, outputName, fileType="csv"):
    outPath = ".\\tests\\" + outputName
    if(not os.path.exists(outPath)):
        os.makedirs(outPath + "\\")
    allPoints = fm.getDataFromFile(fileName, fileType)
    xMax = np.max(allPoints[:,1])+50
    yMax = np.max(allPoints[:,2])+50
    
    #for path of fish
    pl.figure()
    pl.rcParams.update({'font.size': 20})
    pl.plot(allPoints[:,1],allPoints[:,2])
    if(fileType == "csv"):
        pl.axis([0, xMax, 0, yMax])
    else:
        pl.axis([0, xMax, -50, yMax])
    pl.xlabel("x")
    pl.ylabel("y")
    pl.title("Path of Fish")
    pl.savefig(outPath + "\\"+ outputName + "_FishPath.jpg", bbox_inches="tight")
    
    #for time in top
    timeTop = 0
    timeBottom = 0
    if allPoints[0][2] > middle:
        timeTop = timeTop + allPoints[0][0]
    else:
        timeBottom = timeBottom + allPoints[0][0]
    index = 1
    end = np.shape(allPoints)[0]
    while index < end:
        if allPoints[index][2] > middle:
            timeTop = timeTop + (allPoints[index][0] - allPoints[index - 1][0])
        else:
            timeBottom = timeBottom + (allPoints[index][0] - allPoints[index - 1][0])
        index = index + 1
    
    print(timeTop)
    print(timeBottom)
    print(timeTop+timeBottom)
    
endPoints("newTest.csv", 180, "little fish", fileType="csv")