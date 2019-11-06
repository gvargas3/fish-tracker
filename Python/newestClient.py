# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 20:29:20 2019

@author: Brent
"""

#!/usr/bin/env python
import socket, time, os
import winwifi as ww

def Tcp_connect( HostIp, Port ):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
   
def Tcp_Write(D):
    D = D.encode()
    s.send(D)
    return 
   
def Tcp_Read( ):
    b = ''
    a = s.recv(1)
    while (a != b'~' or b == ''):
        b = b + a.decode()
        a = s.recv(1)
    return b

def Tcp_ReadNew( ):
    b = ''
    s.settimeout(2)
    try:
        a = s.recv(1024)
        while(a):
            b = b + a.decode()
            a = s.recv(1024)
        return b
    except socket.timeout:
        return "Failed"

def checkConnection():
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write("Are you there?~")
    s.settimeout(2)
    try:      
        confirmation = Tcp_ReadNew()
        if(confirmation == "Yea boi"):
            return True
        else:
            return False
    except socket.timeout:
        return False

def getPicture():
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('gimmePic~')
    text='.\\' + AP_NAME + '_frame.jpg'
    f = open(text, 'wb')
    s.settimeout(10)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        return text
    except socket.timeout:
        f.close()
        return ""
    
def startVideo(t, name):
    print("trying video")
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('Start video'+'~')
    s.settimeout(2)
    try:      
        confirmation = Tcp_ReadNew()
        if(confirmation == "Time?"):
            Tcp_connect( '169.254.0.1', 5005)
            Tcp_Write(str(t)+'~')
            s.settimeout(2)
            try:      
                confirmation = Tcp_ReadNew()
                if(confirmation == "Name?"):
                    Tcp_connect( '169.254.0.1', 5005)
                    Tcp_Write(name+'~')
                    s.settimeout(2)
                    try:      
                        confirmation = Tcp_ReadNew()
                        if(confirmation == "Recording"):
                            if(not os.path.exists(".\\tests\\" + name)):
                                os.makedirs(".\\tests\\" + name + "\\")
                            return True
                        else:
                            return "Error in giving the name"
                    except socket.timeout:
                        return "Error in giving the name"
                else:
                    return "Error in giving the time"
            except socket.timeout:
                return "Error in giving the time"
        else:
            return "Couldn't send command"
    except socket.timeout:
        return "Couldn't send command"
    
def getDone():
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('Get Completed'+'~')
    numDone = int(Tcp_ReadNew())
    
    print(numDone)
    while (numDone > 0):
        
        numDone = numDone - 1
    
    return True
    
    
def Tcp_Close( ):
   s.close()
   return 
   
def areYouBoard( ):
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('Are You Bored?'+'~')
    
    response = Tcp_ReadNew()
    if response == "Yes I am":
        return True
    else:
        return False
# =============================================================================
# x = ww.WinWiFi()
# AP_NAME = x.get_connected_interfaces()[0]._ssid
# 
# if(checkConnection()):
#     print("connected")
# if(getPicture()):
#     print("Gotpic")
# 
# t = 10
# testName = 'test3'
# print(startVideo(t, testName))
# 
# print(getDone())
# 
# Tcp_Close()
# =============================================================================
