'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午10:21
'''

import configparser

class Setting(object):

    def __init__(self, configFile=None,
                 keysList=[
                     'SUBSCRIBE_URL',
                     'SSR_LIST_JSON',
                     'CONFIG_JSON',
                     'LOCAL_ADDRESS',
                     'TIMEOUT',
                     'WORKERS',
                     'SHADOWSCOKSR_PID',
                     'SHADOWSOCKSR_LOG'
                 ]):
        self.configFile = configFile
        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)
        self.valueDict = self.getAllValue(keysList)

    def getValue(self, key):
        return self.config.get('default', key)

    def setValue(self, key, value):
        self.config.set('default', key, str(value))
        with open(self.configFile, 'w+') as file:
            self.config.write(file)

    def getAllValue(self, keysList):
        valuesDict = dict()
        for key in keysList:
            valuesDict[key] = self.getValue(key)
        return valuesDict
