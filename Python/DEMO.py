# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:19:29 2019

@author: Brent
"""
import pythonMethodsDEMO as pm
import endPointsDEMO
import trackingDEMO
import cv2
import time

while 1:
    key = input()
    
    
    if key == 'p':
        pm.getPicture("Tank01")
        time.sleep(1)       
        im = cv2.imread('frame.jpg')
        cv2.imshow("DEMO",im)
        cv2.waitKey()
    elif key == 'v':
        pm.startVideo("Tank01",20,"DEMO")
    elif key == 'g':
        pm.getVideo("Tank01","DEMO")
    elif key == 't':
        trackingDEMO.trackVideo(".\\tests\\DEMO\\DEMO.mp4","brown.jpg",".\\tests\\DEMO\\DEMO")
        time.sleep(1)
        endPointsDEMO.endPoints("DEMO", "DEMO", path=".\\tests\\DEMO\\",fileType= "csv")
        im = cv2.imread('.\\tests\\DEMO\\DEMO_FishPath.jpg')
        cv2.imshow("Path",im)
        cv2.waitKey()
    elif key == 'x':
        break









#trackVideo(".\\tests\\TEST2\\TEST2.mp4","brown.jpg",".\\tests\\TEST2\\TEST2")