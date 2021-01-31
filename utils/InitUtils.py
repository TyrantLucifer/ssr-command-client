'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午7:52
'''

from logger.Logging import *
import os
import sys
import json
import configparser
import platform
import yaml

class InitConfigDir(object):

    def __init__(self):
        self.version = '2.1.0'
        self.platform = sys.platform
        self.system = platform.system()
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
        self.debugLogFilePath = os.path.join(self.configDir,
                                        'shadowsocksrDebug.log')
        self.ssrListJsonFile = os.path.join(self.configDir,
                                            'ssr-list.json')
        self.ssrJsonFile = os.path.join(self.configDir,
                                        'config.json')
        self.pacFilePath = os.path.join(self.configDir,
                                        'autoproxy.pac')
        self.clashConfigFilePath = os.path.join(self.configDir,
                                                'clashConfig.yaml')
        self.subscribeUrl = 'https://tyrantlucifer.com/ssr/ssr.txt'
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
        logFileHandler = logging.FileHandler(self.logFilePath)
        logFileHandler.setLevel(logging.DEBUG)
        logFileHandler.setFormatter(formatter)
        logger.addHandler(logFileHandler)
        debugFileHandler = logging.FileHandler(self.debugLogFilePath)
        debugFileHandler.setLevel(logging.ERROR)
        debugFileHandler.setFormatter(formatter)
        ssrLogger.addHandler(debugFileHandler)

    def _initConfigFile(self):
        config = configparser.ConfigParser()
        config.add_section('default')
        config.set('default', 'subscribe_url', self.subscribeUrl)
        config.set('default', 'server_json_file_path', self.ssrListJsonFile)
        config.set('default', 'config_json_file_path', self.ssrJsonFile)
        config.set('default', 'local_address', self.localAddress)
        config.set('default', 'timeout', str(self.timeout))
        config.set('default', 'workers', str(self.workers))
        config.set('default', 'shadowsocksr_pid_file_path', self.pidFilePath)
        config.set('default', 'shadowsocksr_log_file_path', self.logFilePath)
        with open(self.configFilePath, 'w+') as file:
            config.write(file)
        with open(self.configLockFilePath, 'w') as lockFile:
            lockFile.write('')

    def _createConfigDir(self):
        os.mkdir(self.configDir)
        with open(self.configFilePath, 'w') as file:
            file.write('')
        self._initConfigFile()

    def createJsonFile(self, ssrDict):
        content = json.dumps(ssrDict, ensure_ascii=False, indent=4)
        with open(self.ssrJsonFile, 'w', encoding='utf-8') as file:
            file.write(content)
