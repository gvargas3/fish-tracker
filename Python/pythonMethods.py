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
import trackingTest
import endPoints
HOST_IP_ADDRESS = '169.254.0.1'
PORT_NUM = 5005

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
        x.connect(ssid)
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

def getPicture(boardName):
    return 'images\\test.jpg'
    # connectForAction(boardName)
    # Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    # Tcp_Write('gimmePic~')
    # text='.\\tests\\frame.jpg'
    # f = open(text, 'wb')
    # s.settimeout(10)
    # try:       
    #     l = s.recv(1024)
    #     while (l):
    #         f.write(l)
    #         l = s.recv(1024)
    #     f.close()
    #     disconnect(boardName)
    #     return text
    # except socket.timeout:
    #     f.close()
    #     disconnect(boardName)
    #     return "failed"
    
def startVideo(boardName, t, name, midpoint=0.5):
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
            try:      
                confirmation = Tcp_ReadNew()
                if(confirmation == "Name?"):
                    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
                    Tcp_Write(name+'~')
                    s.settimeout(2)
                    try:      
                        confirmation = Tcp_ReadNew()
                        if(confirmation == 'Midpoint?'):
                            Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
                            Tcp_Write(str(midpoint)+'~')
                            s.settimeout(2)
                            try: 
                                confirmation = Tcp_ReadNew()
                                if(confirmation == "Recording"):
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
    
def getCsv(boardName, name):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write("GET" + name + "/" + name + ".csv" + "~")
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
        disconnect(boardName)
        return True
    except socket.timeout:
        f.close()
        disconnect(boardName)
        return False

def getVideo(boardName, name):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write("GET" + name + "/" + name + ".mp4" + "~")
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
        disconnect(boardName)
        return True
    except socket.timeout:
        f.close()
        disconnect(boardName)
        return False
    
    
def getDone(boardName):
    connectForAction(boardName)
    Tcp_connect( HOST_IP_ADDRESS, PORT_NUM)
    Tcp_Write('Get Completed'+'~')
    done = Tcp_ReadNew()
    
    doneList = done.split('?')
    print(doneList)
    disconnect(boardName)
    return doneList
    
    
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
    
    #['Connection 1', 'Connection 2', 'Connection 3']
    print(connectionArray)
    return  connectionArray

def connect(ssid):
    x = ww.WinWiFi()
    try:
        x.connect(ssid)
        return True
    except:
        return False
def saveCompletedTest(c):
    data = {}
    data['tests'] = []
    data['tests'].append({
        'board': 'Board 1',
        'duration': '60 minutes',
        'time': 'Noon'
    })

    with open('temp\\completed-tests.txt', 'w') as outfile:
        json.dump(data, outfile)
        
def giveCoords(array):
    return

#print(connectToBoard("Tank01"))
#print(connectToBoard("Tank01"))
# =============================================================================
#print(getPicture("Tank01"))
# time.sleep(5)
#print(startVideo("Tank01",20,"newerTest",0.25))
# time.sleep(20)
# =============================================================================
# =============================================================================
# endPoints.endPoints('newestTest','newestTest',path=".\\tests\\newestTest\\")
# =============================================================================
# =============================================================================
# theseDone = getDone('Tank01')
# for x in theseDone:
#     if x != 'Failed' and x != 'Nothing Here':
#         time.sleep(1)
#         getVideo('Tank01',x)
#         time.sleep(1)
#         getCsv('Tank01',x)
#         time.sleep(1)
#         endPoints.endPoints(x,x,path=".\\tests\\")
# =============================================================================
#print(getVideo("Tank01","newerTest"))
#print(getCsv("Tank01","newerTest"))
endPoints.endPoints('newerTest','newerTest',path=".\\tests\\"+'newerTest\\')

#print(connectNetwork("It Hurts When IP"))