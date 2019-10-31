from __future__ import print_function
import os
import cv2

def getConnections(c):
    #Some code to query what PI boards are available and gets their names
    connectionArray = ['Connection 1', 'Connection 2', 'Connection 3']
    return  connectionArray

def connect(self,c):
    #Need code to connect to the PI, c is the name of the wiFi connection the user chose
    return c