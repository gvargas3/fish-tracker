# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:27:13 2019

@author: Brent
"""
import matplotlib.pyplot as pl
import fileManipulation as fm
import numpy as np
import os
import bisect

# change this path or add one
DEBUG_PATH = "fish-tracker/"
DEBUG_CSV_PATH = "fish-tracker/Python"
PATH = "Python/"

def endPoints(fileName, middle, outputName, fileType="csv"):
    debug = False
    outPath = DEBUG_PATH if debug else ""+outputName
    if(not os.path.exists(outPath)):
        os.makedirs(outPath + "/")
    allPoints = fm.getDataFromFile(DEBUG_CSV_PATH if debug else PATH+fileName, fileType)
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
    pl.savefig(outPath + "/"+ outputName + "_FishPath.jpg", bbox_inches="tight")
    
    #number of entries to the top, 
    # 
    timeTop = 0
    timeBottom = 0
    if allPoints[0][2] > middle:
        timeTop = timeTop + allPoints[0][0]
    else:
        timeBottom = timeBottom + allPoints[0][0]
    index = 1
    end = np.shape(allPoints)[0]

    #should be a way to do a logical operation to calculate the keys with values that corresponde to the endpoint's condition
    #bisect operations?

    # detect latency to the top (above middle)
    firstCross = True
    topEntries = 0
    bottomEntries = 0

    while index < end:

        # top latency & time in top & bottom
        if allPoints[index][2] >= middle:
            if firstCross:
                topLatency = allPoints[index][0]
                firstCross = False
            timeTop = timeTop + (allPoints[index][0] - allPoints[index - 1][0])
        else:
            timeBottom = timeBottom + (allPoints[index][0] - allPoints[index - 1][0])
        totalTime = timeTop + timeBottom # you'd think

        
        # number of entries to the top & bottom
        if allPoints[index][2] >= middle and allPoints[index-1][2] < allPoints[index][2]:
            topEntries = topEntries + 1


        index = index + 1


    print(firstCross,topEntries,bottomEntries,topLatency,timeTop,timeBottom,totalTime)
    # top latency

    #

    #

    #

endPoints("newTest.csv", 180, "newTest", fileType="csv")