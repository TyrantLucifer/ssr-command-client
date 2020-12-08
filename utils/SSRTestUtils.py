'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/7 上午12:14
'''

import socks
import socket
import sys
from multiprocessing import Pool

sys.path.append('../')

from logger.Logging import *
from speedtest import speedtest
from utils.PrintUtils import *

color = Colored()

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
        portStatus, ping = self.isValidConnect(ssrDict['server'],
                                               int(ssrDict['server_port']))
        if ping == '∞':
            ping = color.red(ping)
        else:
            ping = color.green(ping)
        if portStatus:
            portStatus = color.green('True')
        else:
            portStatus = color.red('False')
        ssrDict['ping'] = ping
        ssrDict['port_status'] = portStatus
        return ssrDict

    def testSSRSpeed(self, ssrDict, *args):
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
        return ssrDict

    @calculate
    def threadPool(self, func, args):
        threadList = list()
        pool = Pool(len(args))
        for arg in args:
            thread = pool.apply_async(func, (arg,))
            threadList.append(thread)
        pool.close()
        pool.join()
        return threadList
