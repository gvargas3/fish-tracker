# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:11:47 2019

@author: Brent
"""

import winwifi as ww
import time
import socket
import os
import json
import tracking
import endPoints
HOST_IP_ADDRESS = '169.254.0.1'
PORT_NUM = 5005


# Gets a picture from the Pi's current view for lining up the picture
def getPicture(boardName):
    print('connecting to board')
    connectForAction(boardName)
    print('now trying tcp')
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write('gimmePic~')
    print('selecting file')
    text='.\\tests\\frame.jpg'
    print(text)
    f = open(text, 'wb')
    s.settimeout(5)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        disconnect(boardName)
        return True
    except socket.timeout:
        f.close()
        disconnect(boardName)
        return False
    
# Sends command to start recording a video on the Pi
def startVideo(boardName, t, name, midpoint=0.5):
    print(boardName," ",time,' ',name,' ',midpoint)
    connectForAction(boardName)
    print("trying video")
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write('Start video'+'~')
    s.settimeout(2)
    print("sent command")
    try:      
        confirmation = Tcp_ReadNew()
        if(confirmation == "Time?"):
            Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
            Tcp_Write(str(t)+'~')
            s.settimeout(2)
            print('time: ',t )
            try:      
                confirmation = Tcp_ReadNew()
                if(confirmation == "Name?"):
                    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
                    Tcp_Write(name+'~')
                    print('name: ',name)
                    s.settimeout(2)
                    try:      
                        confirmation = Tcp_ReadNew()
                        if(confirmation == 'Midpoint?'):
                            Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
                            Tcp_Write(str(midpoint)+'~')
                            s.settimeout(2)
                            print('midpoint: ',midpoint)
                            try: 
                                confirmation = Tcp_ReadNew()
                                if(confirmation == "Recording"):
                                    print('recording video')
                                    if(not os.path.exists(".\\tests\\" + name)):
                                        os.makedirs(".\\tests\\" + name + "\\")
                                    disconnect(boardName)
                                    return True
                                else:
                                    disconnect(boardName)
                                    return "Error in giving the name"
                            except socket.timeout:
                                disconnect(boardName)
                                return "Error in giving midpoint"
                        else:
                            disconnect(boardName)
                            return "Error in giving midpoint"
                    except socket.timeout:
                        disconnect(boardName)
                        return "Error in giving the name"
                else:
                    disconnect(boardName)
                    return "Error in giving the time"
            except socket.timeout:
                disconnect(boardName)
                return "Error in giving the time"
        else:
            disconnect(boardName)
            return "Couldn't send command"
    except socket.timeout:
        disconnect(boardName)
        return "Couldn't send command"
  
# Saves the specified csv from the Pi to the computer
def getCsv(boardName, name):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write("GET" + name + "/" + name + ".csv" + "~")
    text = '.\\tests\\' + name
    if(not os.path.exists(text)):
        os.makedirs(".\\tests\\" + name + "\\")
    f = open(text + "\\" + name + ".csv", 'wb')
    s.settimeout(5)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        disconnect(boardName)
        return True
    except socket.timeout:
        f.close()
        disconnect(boardName)
        return False

# Saves the specified video from the Pi to the computer
def getVideo(boardName, name):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write("GET" + name + "/" + name + ".mp4" + "~")
    text = '.\\tests\\' + name
    if(not os.path.exists(text)):
        os.makedirs(".\\tests\\" + name + "\\")
    f = open(text + "\\" + name + ".mp4", 'wb')
    s.settimeout(5)
    try:       
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        disconnect(boardName)
        return True
    except socket.timeout:
        f.close()
        disconnect(boardName)
        return False
    
# Deletes all data related to a specified test on the Pi
def deleteVideo(boardName, name):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write("Delete" + name + "~")
    response = Tcp_ReadNew()
    disconnect(boardName)
    if response == "Deleting":
        time.sleep(3)
        return True
    else:
        return False  
   
# Returns a list of all available tests saved on the Pi
def getDone(boardName):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write('Get Completed'+'~')
    done = Tcp_ReadNew()
    
    doneList = done.split('?')
    #print(doneList)
    disconnect(boardName)
    return doneList




'''
These commands are all for connecting and verifying the board.
These should not be changed.
'''
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
        last = x.get_connected_interfaces()[0]._ssid
        x.connect(ssid)
        try:           
            Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
            Tcp_Write('Are You Bored?'+'~')
    
            response = Tcp_ReadNew()
            if response == "Yes I am":
                disconnect(ssid)
                return "connected"
            else:
                if(last != ssid):
                    disconnect(ssid)
                return "not a board"
        except:
            time.sleep(0.5)
            print(last,ssid)
            if(last != ssid):
                disconnect(ssid)
            return "could not connect socket"
    except:
        if(last != ssid):
            disconnect(ssid)
        return "could not connect to access point"
    
def connectForAction(ssid):
    x = ww.WinWiFi
    try:
        time.sleep(3)
        x.connect(ssid)
        time.sleep(3)
        print('connected')
        return True
    except:
        time.sleep(1)
        disconnect(ssid)
        return False
    
def disconnect(boardName):
    x = ww.WinWiFi
    current = x.get_connected_interfaces()[0]._ssid
    if current == boardName:       
        try:
            x.disconnect()
            return True
        except:
            return False
    else:
        return "wasn't connected to board"
    
def Tcp_connect( HostIp, Port ):
    global s
    time.sleep(3)
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

def Tcp_Close( ):
   s.close()
   return 
   
def areYouBoard(boardName):
    #connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write('Are You Bored?'+'~')
    
    response = Tcp_ReadNew()
    if response == "Yes I am":
        disconnect(boardName)
        return "connected"
    else:
        disconnect(boardName)
        return "not a board"  
    
def getConnections(c):
    #Some code to query what PI boards are available and gets their names
    x = ww.WinWiFi()
    netList = x.scan()
    connectionArray=[]
    for p in netList:
        if p._ssid!='':
            connectionArray.append(p._ssid)
    print(connectionArray)
    return  connectionArray
#print(connectToBoard("Tank01"))
#print(connectToBoard("Tank01"))
# =============================================================================
#print(getPicture("Tank01"))
# time.sleep(5)
#print(startVideo("Tank01",30,"TEST2",0.6))
# time.sleep(20)
# ============================================================================
#print(getDone('Tank01'))
#print(deleteVideo('Tank01','newerTest'))
# =============================================================================
# print(deleteVideo('Tank01','TEST2'))
# print(deleteVideo('Tank01','newestTest'))
# print(deleteVideo('Tank01','thisTest'))
# print(deleteVideo('Tank01','newerTest'))
# print(getDone('Tank01'))
# =============================================================================
# =============================================================================
# endPoints.endPoints('newestTest','newestTest',path=".\\tests\\newestTest\\")
# =============================================================================
# =============================================================================
#theseDone = getDone('Tank01')
# for x in theseDone:
#     if x != 'Failed' and x != 'Nothing Here':
#         time.sleep(1)
#         getVideo('Tank01',x)
#         time.sleep(1)
#         getCsv('Tank01',x)
#         time.sleep(1)
#         endPoints.endPoints(x,x,path=".\\tests\\")
# =============================================================================
#print(getVideo("Tank01","TEST2"))
#print(getCsv("Tank01","TEST1"))
#print(getVideo("Tank01","TEST1"))
#x = 'test1'

#endPoints.endPoints(x,x,path=".\\tests\\"+x+'\\')
# =============================================================================
# x = 'nothing'
# while x == 'nothing':
#     try:
#         x=getDone('Tank01')
#         print(x)
#     except:
#         print(x)
#         disconnect('Tank01')
#         time.sleep(60)
# =============================================================================
#print(connectNetwork("It Hurts When IP"))