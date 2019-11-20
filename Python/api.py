from __future__ import print_function
from calc import calc as real_calc
import connectionstringtest as connection
import pythonMethods as pm
import giveCoords as coords
import fileManipulation as fileManip
import trackingTest as tt
#import newestClient as nc
import sys
import zerorpc

class CalcApi(object):
    def calc(self, text):
        """based on the input text, return the int result"""
        try:
            print('In calculator')
            return real_calc(text)
        except Exception as e:
            return 0.0
    def getConnections(self):
        try:
            return connection.getConnections(self)
        except Exception as e:
            return 0.0
    def connectToBoard(self, connectionName):
        try:
            return pm.connectToBoard(connectionName)
        except Exception as e:
            return 0.0
    def saveCompletedTest(self):
        try:
            connection.saveCompletedTest(self)
        except Exception as e:
            return e
    def getPicture(self, boardName):
        try:
            return pm.getPicture(boardName)
        except Exception as e:
            return e
    def giveCoords(self, array):
        try:
            return coords.giveCoords(array)
        except Exception as e:
            return e
    def getCurrentNetwork(self):
        try:
            return pm.getCurrentNetwork()
        except Exception as e:
            return e
    def connectNetwork(self, ssid):
        try:
            return pm.connectNetwork(ssid)
        except Exception as e:
            return e
    def startVideo(self,boardName, t,name):
        try: 
            return pm.startVideo(boardName, t,name)
        except Exception as e:
            return e
    def getDataFromFile(self,path,fileType="csv"):
        try:
            return fileManip.getDataFromFile(path,fileType)
        except Exception as e:
            return e
    def echo(self, text):
        print('called Echo method')
        """echo any text"""
        return text

def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)

def main():
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(CalcApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
