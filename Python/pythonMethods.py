# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:11:47 2019

@author: Brent
"""

import winwifi as ww
import newestClient as nc

def getCurrentNetwork():
    x = ww.WinWiFi
    text = x.get_connected_interfaces()
    if(text != []):
        text = text[0]._ssid
    return text

def connectNetwork(ssid):
    x = ww.WinWiFi
    try:
        x.connect(ssid)
        return True
    except:
        return False
    
def connectToBoard(ssid):
    x = ww.WinWiFi
    try:
        x.connect(ssid)
        return nc.areYouBoard()
    except:
        return False