# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:27:13 2019

@author: Brent
"""
import fileManipulation as fm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as mcoll
import matplotlib.path as mpath
import os
import bisect

# change this path or add one
DEBUG_PATH = "fish-tracker/"
DEBUG_CSV_PATH = "fish-tracker/Python"
#PATH = "Python/"
PATH = "tests/"

def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0), linewidth=4, alpha=1.0):
    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc

def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments


def endPoints(fileName, middle, outputName, fileType="csv"):
    debug = False
    outPath = DEBUG_PATH if debug else PATH + outputName
    if(not os.path.exists(outPath)):
        os.makedirs(outPath + "/")
    allPoints = fm.getDataFromFile(DEBUG_CSV_PATH if debug else fileName, fileType)
    xMax = np.max(allPoints[:,1])+50
    yMax = np.max(allPoints[:,2])+50
    duration = allPoints[-1][0]/1000
    duration = np.round(duration, decimals=1)
    
    #for path of fish  
    plt.figure(figsize=(10,10))
    x = allPoints[:,1]
    y = allPoints[:,2]
    lc = colorline(x, y, cmap='cool')
    cbar = plt.colorbar(lc,orientation='horizontal',pad=0.15,ticks=[0,.25,.5,.75,1])
    cbar.set_ticklabels([0,duration/4,duration/2,3*duration/4,duration])
    cbar.set_label("Time (minutes)")
    if(fileType == "csv"):
        plt.axis([0, xMax, 0, yMax])
    else:
        plt.axis([0, xMax, -50, yMax])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Path of Fish")
    plt.savefig(outPath + "/"+ outputName + "_FishPath.jpg", bbox_inches="tight")
    plt.show()
    
    
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

        if allPoints[index][2] <= middle and allPoints[index-1][2] > allPoints[index][2]:
            bottomEntries = bottomEntries + 1


        index = index + 1


    print(topEntries,bottomEntries,topLatency,timeTop,timeBottom,totalTime)
    
    labels = 'Top', 'Bottom'
    sizes = [timeTop, timeBottom]
    fig1, ax1 = plt.subplots(figsize=(7,5))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
             startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Time Spent")
    plt.show() #this will show the original path plot brent made and the pie
    # the gradient plot is commented out for now. Cant seem to get it to work like how I want yet

    # top latency

    #

    #

    #

endPoints("newTest.csv", 180, "newTest1", fileType="csv")