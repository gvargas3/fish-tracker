# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:50:18 2019

@author: Brent
"""
import numpy as np


def getDataFromFile(filePath, fileType="csv"):
    if fileType == "csv":
        try:       
            array = np.loadtxt(filePath + ".csv",delimiter=',')
            middle = np.max(array[:,2])/2
            if array[0,0] == 1000:
                middle = array[0,1]
                array = array[1:]
            print("center at ",middle)
            return array, middle
        except:
            return "couldn't load file"
        
    elif fileType == "txt":
        try:          
            array= np.loadtxt(filePath + ".txt", delimiter='\t', usecols=(0, 1, 2))
            x = np.where(array[:,1] == -1)
            x = np.array(x)
            x = x.flatten()
            array = np.delete(array,x,0)
            yMax = np.max(array[:,2])
            array[:,2] = yMax - array[:,2]
            print("Center at ",np.max(array[:,2])/2)
            return array, np.max(array[:,2])/2
        except:
            return "couldn't load file"
    else:
        return "Invalid Data Type"
#getDataFromFile('testes.csv','csv')