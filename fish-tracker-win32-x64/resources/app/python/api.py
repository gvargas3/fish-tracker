from __future__ import print_function
from calc import calc as real_calc
import connectionstringtest as connection
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
            return connection.connect(self, connectionName)
        except Exception as e:
            return 0.0
    def saveCompletedTest(self):
        try:
            connection.saveCompletedTest(self)
        except Exception as e:
            return e
    def getScreenshot(self):
        try:
            return connection.getScreenshot(self)
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
