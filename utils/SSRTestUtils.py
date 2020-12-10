'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/7 上午12:14
'''

import socks
import socket
import sys
from . import multiprocessing_win

from multiprocessing import Pool, Process
import multiprocessing.pool

sys.path.append('../')

from speedtest import speedtest
from utils.PrintUtils import *
from utils.HandleSSRUtils import *

c = ControlSSR()
color = Colored()

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

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
            logger.debug(e)
            logger.debug('Server: {0}  Port: {1} is invalid'. \
                         format(server, port))
            s.close()
            return False, '∞'
        else:
            delay = (endTime - startTime).microseconds / 1000
            return True, str(delay)

    def testSSRConnect(self, ssrDict):
        connect, ping = self.isValidConnect(ssrDict['server'],
                                               int(ssrDict['server_port']))
        ssrDict['ping'] = ping
        ssrDict['connect'] = connect
        return ssrDict

    def testSSRSpeed(self, ssrDict, *args):
        if ssrDict['connect']:
            p = Process(target=c.startOnWindows, args=(ssrDict, *args))
            p.daemon = True
            p.start()
            socks.set_default_proxy(socks.SOCKS5, args[0], args[1])
            socket.socket = socks.socksocket
            try:
                s = speedtest.Speedtest()
                s.upload()
                s.download()
            except Exception as e:
                logger.debug(e)
                logger.debug("This ssr node is invalid")
                download = '∞'
                upload = '∞'
            else:
                result = s.results.dict()
                download = round(result['download'] / 1000.0 / 1000.0, 2)
                upload = round(result['upload'] / 1000.0 / 1000.0, 2)
            ssrDict['download'] = download
            ssrDict['upload'] = upload
        else:
            ssrDict['download'] = '∞'
            ssrDict['upload'] = '∞'

        return ssrDict

    @calculate
    def connectThreadPool(self, func, args):
        multiprocessing.freeze_support()
        threadList = list()
        pool = Pool(len(args))
        for arg in args:
            thread = pool.apply_async(func, (arg,))
            threadList.append(thread)
        pool.close()
        pool.join()
        return threadList

    @calculate
    def speedThreadPool(self, func, args):
        multiprocessing.freeze_support()
        port = 60000
        threadList = list()
        pool = MyPool(len(args))
        for arg in args:
            thread = pool.apply_async(func, (arg, '127.0.0.1', port, 300, 1))
            threadList.append(thread)
            port = port + 1
        pool.close()
        pool.join()
        return threadList

    @calculate
    def startConnectTest(self, ssrDictList):
        result = list()
        threadList = self.connectThreadPool(self.testSSRConnect, ssrDictList)
        for thread in threadList:
            result.append(thread.get())
        return result

    @calculate
    def startSpeedTest(self, ssrDictList):
        result = list()
        threadList = self.speedThreadPool(self.testSSRSpeed, ssrDictList)
        for thread in threadList:
            result.append(thread.get())
        return result