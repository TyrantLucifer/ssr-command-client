'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/7 上午12:14
'''

from logger.Logging import *
import socket
import datetime
from progressbar import *

class SsrSpeedTest(object):

    def __init__(self):
        pass

    def isValidConnect(self, server, port):
        serverAddr = (server, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        startTime = datetime.datetime.now()
        try:
            s.connect(serverAddr)
            endTime = datetime.datetime.now()
        except Exception as e:
            logger.error(e)
            logger.error('Server: {0}  Port: {1} is invalid'.\
                         format(server, port))
            s.close()
            return False, '∞'
        else:
            delay = (endTime - startTime).microseconds / 1000
            return True, str(delay)

    def testSsrNodes(self, ssrDict):
        portStatus, ping = self.isValidConnect(ssrDict['server'],
                                               int(ssrDict['server_port']))
        ssrDict['ping'] = ping
        ssrDict['port_status'] = portStatus
        return ssrDict
