"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: parse_utils.py
@time: 2021/2/18 19:57
@desc: 提供解析Shadowsocksr节点工具类
"""

import re
import base64
import requests
from shadowsocksr_cli.logger import *


class ParseShadowsocksr(object):
    """解析shadowsocksr节点信息

    该工具类可提供静态方法进行shadowsocksr订阅链接解析

    属性:
        None
    """

    def __init__(self):
        pass

    @staticmethod
    def base64_decode(text):
        """根据ssr节点编码规则，将信息转换成为正确base64编码
        :param text: 待解析的文本
        :return: 转换后的文本
        """
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
    def parse_shadowsocksr(ssr_url):
        """使用shadowsocksr url解析shadowsocksr节点信息
        :param ssr_url: ssr链接，例如"ssr://rexx"
        :return: ssr_dict: 返回ssr信息字典
        """
        ssr_available_url = ssr_url[6:]
        try:
            ssr_decode_url = ParseShadowsocksr.base64_decode(ssr_available_url)
        except Exception as e:
            logger.error(e)
        else:
            ssr_dict = dict()
            param_list = ssr_decode_url.split(':')
            if len(param_list) == 6:
                server = param_list[0]
                port = param_list[1]
                protocol = param_list[2]
                method = param_list[3]
                obfs = param_list[4]
                first_encryption_param_list = param_list[-1].split('/?')
                password = ParseShadowsocksr.base64_decode(first_encryption_param_list[0])
                second_encryption_param_list = first_encryption_param_list[-1].split('&')
                key_list = [
                    'obfs_param',
                    'protocol_param',
                    'remarks',
                    'group'
                ]
                for params in second_encryption_param_list:
                    key = params.split('=')[0]
                    value = params.split('=')[1]
                    if key == 'obfsparam':
                        key = 'obfs_param'
                    if key == 'protoparam':
                        key = 'protocol_param'
                    if key in key_list:
                        ssr_dict[key] = ParseShadowsocksr.base64_decode(value)
                ssr_dict['server'] = server
                ssr_dict['server_port'] = int(port)
                ssr_dict['method'] = method
                ssr_dict['obfs'] = obfs
                ssr_dict['password'] = password
                ssr_dict['protocol'] = protocol
                ssr_dict['ssr_url'] = ssr_url
                ssr_dict['port_password'] = None
                ssr_dict['additional_ports'] = {}
                ssr_dict['additional_ports_only'] = False
                ssr_dict['udp_timeout'] = 120
                ssr_dict['udp_cache'] = 64
                ssr_dict['fast_open'] = False
                ssr_dict['verbose'] = False
                ssr_dict['connect_verbose_info'] = 0
                return ssr_dict
            else:
                logger.debug("Currently it is not support ipv6 node")

    @staticmethod
    def parse_shadowsocksr_by_subscribe_url(subscribe_url):
        """通过shadowsocksr订阅链接解析shadowsocksr节点信息

        :param subscribe_url: shadowsocksr订阅链接
        :return: ssr_dict_list: shadowsocksr节点信息字典列表
        """
        ssr_dict_list = list()
        logger.info('Start parse ssr subscribe url: {0}'.format(subscribe_url))
        try:
            result = requests.get(subscribe_url)
            result.encoding = 'utf-8'
            ssr_result = ParseShadowsocksr.base64_decode(result.text)
        except Exception as e:
            logger.error(e)
            logger.error("Parse subscribe url {0} error".format(subscribe_url))
        else:
            ssr_url_list = ssr_result.split('\n')
            for ssr_url in ssr_url_list:
                if ssr_url:
                    ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
                    if ssr_dict:
                        ssr_dict_list.append(ssr_dict)
        return ssr_dict_list
