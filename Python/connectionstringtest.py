from __future__ import print_function
import os
import json
import winwifi


def getConnections(c):
    #Some code to query what PI boards are available and gets their names
    x = winwifi.WinWiFi()
    netList = x.scan()
    connectionArray=['test']
    for p in netList:
        connectionArray.append(p._ssid)
    
    #['Connection 1', 'Connection 2', 'Connection 3']
    print(connectionArray)
    return  connectionArray

def connect(self,c):
    #Need code to connect to the PI, c is the name of the wiFi connection the user chose
    return c
def saveCompletedTest(self):
    data = {}
    data['tests'] = []
    data['tests'].append({
        'board': 'Board 1',
        'duration': '60 minutes',
        'time': 'Noon'
    })

    with open('temp\\completed-tests.txt', 'w') as outfile:
        json.dump(data, outfile)
def getScreenshot(self):
    #Need code for getting a screenshot from the board
    #Need code for saving that screenshot in the images folder

    filepath = 'images/test.jpg'
    return filepath
#getConnections(0)