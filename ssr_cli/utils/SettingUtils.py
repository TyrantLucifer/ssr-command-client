'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午10:21
'''

import configparser

class Setting(object):

    def __init__(self, configFile=None,
                 keysList=[
                     'subscribe_url',
                     'server_json_file_path',
                     'config_json_file_path',
                     'local_address',
                     'timeout',
                     'workers',
                     'shadowsocksr_pid_file_path',
                     'shadowsocksr_log_file_path'
                 ]):
        self.keyList = keysList
        self.configFile = configFile
        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)
        self.valueDict = self.getAllValue(keysList)
        self.subscribe_url = self.valueDict['subscribe_url']
        self.local_address = self.valueDict['local_address']
        self.timeout = int(self.valueDict['timeout'])
        self.workers = int(self.valueDict['workers'])

    def getValue(self, key):
        return self.config.get('default', key)

    def setValue(self, key, value):
        self.config.set('default', key, str(value))
        with open(self.configFile, 'w+') as file:
            self.config.write(file)
        self.getAllValue(self.keyList)

    def getAllValue(self, keysList):
        valuesDict = dict()
        for key in keysList:
            valuesDict[key] = self.getValue(key)
        self.valueDict = valuesDict
        self.subscribe_url = self.valueDict['subscribe_url']
        self.local_address = self.valueDict['local_address']
        self.timeout = int(self.valueDict['timeout'])
        self.workers = int(self.valueDict['workers'])
        return valuesDict
