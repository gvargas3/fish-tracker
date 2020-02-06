from __future__ import print_function
import pythonMethods as pm
import fileManipulation as fileManip
import sys
import zerorpc

class CalcApi(object):
    def getConnections(self):
        try:
            return pm.getConnections(self)
        except:
            return 0.0
    def connectToBoard(self, connectionName):
        try:
            return pm.connectToBoard(connectionName)
        except:
            return 0.0
    def getPicture(self, boardName):
        try:
            print('trying')
            return pm.getPicture(boardName)
            print('tried')
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
    def startVideo(self,boardName, t,name, midpoint=0.5):
        try: 
            return pm.startVideo(boardName, t,name,midpoint)
        except Exception as e:
            return e
    def getDataFromFile(self,path,fileType="csv"):
        try:
            return fileManip.getDataFromFile(path,fileType)
        except Exception as e:
            return e
    def downloadResults(self):
        try:
            return pm.downloadResults()
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
    except:
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
