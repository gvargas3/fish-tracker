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
import matplotlib
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


def endPoints(fileName, outputName, path="", fileType="csv"):
    matplotlib.rcParams.update({'font.size': 22}) 
    debug = False
    outPath = DEBUG_PATH if debug else path + outputName
    if(not os.path.exists(outPath)):
        os.makedirs(outPath + "/")
    allPoints, middle = fm.getDataFromFile(DEBUG_CSV_PATH if debug else path + fileName, fileType)
    xMax = np.max(allPoints[:,1])+50
    yMax = np.max(allPoints[:,2])+50
    duration = allPoints[-1][0]/60000
    duration = np.round(duration, decimals=1)
    
    #for path of fish  
    plt.figure(figsize=(10,10))
    x = allPoints[:,1]
    y = allPoints[:,2]
    lc = colorline(x, y, cmap='cool')
    cbar = plt.colorbar(lc,orientation='horizontal',pad=0.15,ticks=[0,.25,.5,.75,1])
    cbar.set_ticklabels([0,np.round(duration/4,decimals=2),duration/2,np.round(3*duration/4,decimals=2),duration])
    cbar.set_label("Time (minutes)")
    if(fileType == "csv"):
        plt.axis([0, 1296, 0, 730])
    else:
        plt.axis([0, xMax, -50, yMax])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Path of Fish")
    plt.savefig(outPath + "_FishPath.jpg", bbox_inches="tight")
    #plt.show()