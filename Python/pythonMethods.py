# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:11:47 2019

@author: Brent
"""

import winwifi as ww
import newestClient as nc
import time
import socket
import os

def getCurrentNetwork():
    x = ww.WinWiFi
    text = x.get_connected_interfaces()
    if(text != []):
        text = text[0]._ssid
    return text

def connectNetwork(ssid):
    x = ww.WinWiFi
    try:
        #x.disconnect()
        #x.scan()
        x.connect(ssid)
        return True
    except:
        return False
    
def connectToBoard(ssid):
    x = ww.WinWiFi
    try:
        x.connect(ssid)
        return areYouBoard()
    except:
        disconnect()
        return "could not connect"
    
def connectForAction(ssid):
    x = ww.WinWiFi
    try:
        x.connect(ssid)
        return True
    except:
        return False
    
def disconnect():
    x = ww.WinWifi
    try:
        x.disconnect
        return True
    except:
        return False
    
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

def checkConnection(boardName):
    connectForAction(boardName)
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write("Are you there?~")
    s.settimeout(2)
    try:      
        confirmation = Tcp_ReadNew()
        if(confirmation == "Yea boi"):
            disconnect()
            return True
        else:
            disconnect()
            return False
    except socket.timeout:
        disconnect()
        return False

def getPicture(boardName):
    connectForAction(boardName)
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('gimmePic~')
    text='.\\tests\\frame.jpg'
    f = open(text, 'wb')
    s.settimeout(10)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        disconnect()
        return text
    except socket.timeout:
        f.close()
        disconnect()
        return ""
    
def startVideo(boardName, t, name):
    connectForAction(boardName)
    print("trying video")
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('Start video'+'~')
    s.settimeout(2)
    print("sent command")
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
                            disconnect()
                            return True
                        else:
                            disconnect()
                            return "Error in giving the name"
                    except socket.timeout:
                        disconnect()
                        return "Error in giving the name"
                else:
                    disconnect()
                    return "Error in giving the time"
            except socket.timeout:
                disconnect()
                return "Error in giving the time"
        else:
            disconnect()
            return "Couldn't send command"
    except socket.timeout:
        disconnect()
        return "Couldn't send command"
    
def getCsv(boardName, name):
    connectForAction(boardName)
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write(name + "/" + name + ".csv" + "~")
    text = '.\\tests\\' + name
    if(not os.path.exists(text)):
        os.makedirs(".\\tests\\" + name + "\\")
    f = open(text + "\\" + name + ".csv", 'wb')
    s.settimeout(10)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        disconnect()
        return True
    except socket.timeout:
        f.close()
        disconnect()
        return False

def getVideo(boardName, name):
    connectForAction(boardName)
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write(name + "/" + name + ".mp4" + "~")
    text = '.\\tests\\' + name
    if(not os.path.exists(text)):
        os.makedirs(".\\tests\\" + name + "\\")
    f = open(text + "\\" + name + ".mp4", 'wb')
    s.settimeout(10)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        disconnect()
        return True
    except socket.timeout:
        f.close()
        disconnect()
        return False
    
    
def getDone(boardName):
    connectForAction(boardName)
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('Get Completed'+'~')
    numDone = int(Tcp_ReadNew())
    
    print(numDone)
    while (numDone > 0):
        
        numDone = numDone - 1
    disconnect()
    return True
    
    
def Tcp_Close( ):
   s.close()
   return 
   
def areYouBoard(boardName):
    connectForAction(boardName)
    Tcp_connect( '169.254.0.1', 5005)
    Tcp_Write('Are You Bored?'+'~')
    
    response = Tcp_ReadNew()
    if response == "Yes I am":
        disconnect()
        return "connected"
    else:
        disconnect()
        return "not a board"

#print(connectNetwork("It Hurts When IP"))