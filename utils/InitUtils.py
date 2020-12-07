'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午7:52
'''

from logger.Logging import *
import os
import sys
import configparser


class InitConfigDir(object):

    def __init__(self):
        self.platform = sys.platform
        self.homeDir = os.path.expanduser('~')
        self.configDir = os.path.join(self.homeDir,
                                      '.ssr-command-client')
        self.configFilePath = os.path.join(self.configDir,
                                           'config.ini')
        self.configLockFilePath = os.path.join(self.configDir,
                                               '.config.lock')
        self.pidFilePath = os.path.join(self.configDir,
                                        'shadowsocksr.pid')
        self.logFilePath = os.path.join(self.configDir,
                                        'shadowsocksr.log')
        self.ssrListJsonFile = os.path.join(self.configDir,
                                            'ssr-list.json')
        self.ssrJsonFile = os.path.join(self.configDir,
                                        'config.json')
        self.subscribeUrl = 'https://tyrantlucifer.com/ssr.txt'
        self.localAddress = '127.0.0.1'
        self.timeout = 300
        self.workers = 1

        if not self._isExistConfigDir():
            self._createConfigDir()
        self._setLogger()

    def _isExistConfigDir(self):
        if os.path.exists(self.configDir):
            return True
        else:
            return False

    def _setLogger(self):
        fileHandler = logging.FileHandler(self.logFilePath)
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    def _initConfigFile(self):
        config = configparser.ConfigParser()
        config.add_section('default')
        config.set('default', 'SUBSCRIBE_URL', self.subscribeUrl)
        config.set('default', 'SSR_LIST_JSON', self.ssrListJsonFile)
        config.set('default', 'CONFIG_JSON', self.ssrJsonFile)
        config.set('default', 'LOCAL_ADDRESS', self.localAddress)
        config.set('default', 'TIMEOUT', str(self.timeout))
        config.set('default', 'WORKERS', str(self.workers))
        config.set('default', 'SHADOWSCOKSR_PID', self.pidFilePath)
        config.set('default', 'SHADOWSOCKSR_LOG', self.logFilePath)
        with open(self.configFilePath, 'w+') as file:
            config.write(file)
        with open(self.configLockFilePath, 'w') as lockFile:
            lockFile.write('')

    def _createConfigDir(self):
        os.mkdir(self.configDir)
        with open(self.configFilePath, 'w') as file:
            file.write('')
        self._initConfigFile()
