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
PATH = "Python/"

def colorline(
    x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
        linewidth=3, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

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
    outPath = DEBUG_PATH if debug else ""+outputName
    if(not os.path.exists(outPath)):
        os.makedirs(outPath + "/")
    allPoints = fm.getDataFromFile(DEBUG_CSV_PATH if debug else PATH+fileName, fileType)
    xMax = np.max(allPoints[:,1])+50
    yMax = np.max(allPoints[:,2])+50
    
    #for path of fish
    plt.figure()
    plt.rcParams.update({'font.size': 20})
    plt.plot(allPoints[:,1],allPoints[:,2])
    colorline(allPoints[:,1],allPoints[:,2], np.linspace(0, 1000, len(allPoints[:,1])), cmap=plt.get_cmap('rainbow'), linewidth=2)
    
    # gradient stuff... why blue?
    # x = allPoints[:,1]
    # y = allPoints[:,2]
    ###nothis fig, ax = plt.subplots()

    # path = mpath.Path(np.column_stack([x, y]))
    # verts = path.interpolated(steps=3).vertices
    # x, y = verts[:, 0], verts[:, 1]
    # z = np.linspace(0, 1.0, 100)
    # colorline(x, y, z, cmap=plt.get_cmap('cool'), linewidth=2)

    # plt.show()

    if(fileType == "csv"):
        plt.axis([0, xMax, 0, yMax])
    else:
        plt.axis([0, xMax, -50, yMax])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Path of Fish")
    plt.savefig(outPath + "/"+ outputName + "_FishPath.jpg", bbox_inches="tight")
    
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

endPoints("newTest1.csv", 180, "newTest1", fileType="csv")