'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/7 上午12:14
'''

import datetime
import socket
import sys
from multiprocessing import Pool

sys.path.append('../')

from logger.Logging import *
from speedtest import speedtest

class SSRSpeedTest(object):

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
            logger.error('Server: {0}  Port: {1} is invalid'. \
                         format(server, port))
            s.close()
            return False, '∞'
        else:
            delay = (endTime - startTime).microseconds / 1000
            return True, str(delay)

    def testSSRConnect(self, ssrDict):
        portStatus, ping = self.isValidConnect(ssrDict['server'],
                                               int(ssrDict['server_port']))
        ssrDict['ping'] = ping
        ssrDict['port_status'] = portStatus
        return ssrDict

    def testSSRSpeed(self, ssrDict):
        s = speedtest.Speedtest()
        s.upload()
        s.download()
        pass

    def threadPool(self, func, args):
        threadList = list()
        pool = Pool(len(args))
        for arg in args:
            thread = pool.apply_async(func, (arg,))
            threadList.append(thread)
        pool.close()
        pool.join()
        return threadList
