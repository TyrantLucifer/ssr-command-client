'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午6:36
'''

from logger.Logging import *
import requests
import base64
import re


class ParseShadowsocksR(object):
    '''
    解析ssr节点工具类
    '''

    def __init__(self):
        pass

    @staticmethod
    def base64Decode(text):
        '''
        根据ssr节点编码规则，将信息转换成为正确base64编码
        :param text: 待解析的文本
        :return: 转换后的文本
        '''
        i = len(text) % 4
        if i == 1:
            text = text + '==='
        elif i == 2:
            text = text + '=='
        elif i == 3:
            text = text + '='
            text = re.sub(r'_', '/', text)
            text = re.sub(r'-', '+', text)
        return base64.urlsafe_b64decode(text).decode()

    @staticmethod
    def parseShadowsocksR(ssrUrl):
        '''
        解析ssr链接
        :param ssrUrl: ssr链接，例如"ssr://xxxxxxx"
        :return: 返回ssr信息字典
        '''
        availableUrl = ssrUrl[6:]
        try:
            decodeUrl = ParseShadowsocksR.base64Decode(availableUrl)
        except Exception as e:
            logger.error(e)
        else:
            ssrDict = dict()
            paramList = decodeUrl.split(':')
            if len(paramList) == 6:
                server = paramList[0]
                port = paramList[1]
                protocol = paramList[2]
                method = paramList[3]
                obfs = paramList[4]
                firstEncryptionParamList = paramList[-1].split('/?')
                password = ParseShadowsocksR.base64Decode(firstEncryptionParamList[0])
                secondEncryptionParamList = firstEncryptionParamList[-1].split('&')
                keyList = [
                    'obfs_param',
                    'protocol_param',
                    'remarks',
                    'group'
                ]
                for params in secondEncryptionParamList:
                    key = params.split('=')[0]
                    value = params.split('=')[1]
                    if key == 'obfsparam':
                        key = 'obfs_param'
                    if key == 'protoparam':
                        key = 'protocol_param'
                    if key in keyList:
                        ssrDict[key] = ParseShadowsocksR.base64Decode(value)
                ssrDict['server'] = server
                ssrDict['server_port'] = int(port)
                ssrDict['method'] = method
                ssrDict['obfs'] = obfs
                ssrDict['password'] = password
                ssrDict['protocol'] = protocol
                ssrDict['ssr_url'] = ssrUrl
                return ssrDict
            else:
                logger.debug("Currently it is not support ipv6 node")


class GetSubscribeUrl(object):

    def __init__(self):
        self.resultList = list()
        self.ssrInfoList = list()

    @staticmethod
    def requestUrl(url):
        try:
            result = requests.get(url)
            result.encoding = 'utf-8'
            ssrResult = ParseShadowsocksR.base64Decode(result.text)
        except Exception as e:
            logger.error(e)
            logger.error("Parse subscribe url error")
        else:
            ssrUrlList = ssrResult.split('\n')
            return ssrUrlList

    def requestUrlList(self, urlList):
        for url in urlList:
            result = self.requestUrl(url)
            self.resultList.append(result)
        return self.resultList

    def getNodeInfoList(self):
        for urlResult in self.resultList:
            for ssrUrl in urlResult:
                if ssrUrl:
                    self.ssrInfoList.append(ParseShadowsocksR.parseShadowsocksR(ssrUrl))
        return self.ssrInfoList
