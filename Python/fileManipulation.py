# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:50:18 2019

@author: Brent
"""
import numpy as np


def getDataFromFile(filePath, fileType="csv"):
    if fileType == "csv":
        try:       
            array = np.loadtxt(filePath,delimiter=',')
            return array
        except:
            return "couldn't load file"
        
    elif fileType == "txt":
        try:          
            array= np.loadtxt(filePath, delimiter='\t', usecols=(0, 1, 2))
            x = np.where(array[:,1] == -1)
            x = np.array(x)
            x = x.flatten()
            array = np.delete(array,x,0)
            return array
        except:
            return "couldn't load file"
    else:
        return "Invalid Data Type"
    
