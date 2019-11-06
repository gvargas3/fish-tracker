# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:11:47 2019

@author: Brent
"""

import winwifi as ww

def getCurrentNetwork():
    x = ww.WinWiFi
    text = x.get_connected_interfaces()
    if(text != []):
        text = text[0]._ssid
    return text
