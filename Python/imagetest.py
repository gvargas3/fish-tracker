from __future__ import print_function
import os
import cv2

def getImage(c):
    print('In this python function')
    image = cv2.imread(os.getcwd() + '/images/test.png')
    im = Image.fromarray(image)
    im.save(os.getcwd() + '/images/test2.png')
    return  image.tolist()