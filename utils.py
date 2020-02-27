#!/usr/bin/env python3
# coding=utf-8

# 导入相关系统包
import requests
import base64
import re
import os
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

class DrawTable(object):
    '''工具类，打印表格格式化'''
    def __init__(self):
        self.table = []
        header = [
            "id",
            "name",
            "ping(ms)",
            "server",
            "port",
            "method"
        ]
        self.x = PrettyTable(header)
        self.x.reversesort = True

    def append(self,*args,**kwargs):
        if(kwargs):
            content=[
                kwargs['id'],
                kwargs['name'],
                kwargs['ping'],
                kwargs['server'],
                kwargs['port'],
                kwargs['method'],
            ]
            self.x.add_row(content)

    def str(self):
        return str(self.x)

init (autoreset=False)
class colored(object):
    '''工具类，打印不同颜色字体'''
    def red(self,s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    def green(self,s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    def yellow(self,s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET
    def blue(self,s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

# 对base编码进行解码
def base64decode(text):
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

# 通过订阅链接获取ssr url链接列表
def get_ssr_list(url):
    color = colored()
    url_colored = color.blue(url)
    print('Being parsed the ssr url:', url_colored)
    print('It will take a moment,Please be patient~~')
    result = requests.get(url)
    ssr_result = base64decode(result.text)
    ssr_list = ssr_result.split('\n')
    ssr_real_list = list()
    for ssr in ssr_list:
        if ssr:
            ssr_real_list.append(ssr[6:])
    return ssr_real_list

# 解析ssr url链接
def analysis_ssr_url(ssr_url):
    ssr_url = base64decode(ssr_url)
    param_list = ssr_url.split(':')
    server = param_list[0]
    port = param_list[1]
    protocol = param_list[2]
    method = param_list[3]
    obfs = param_list[4]
    second_encryption_param_list = param_list[-1].split('/?')
    password = base64decode(second_encryption_param_list[0])
    encryption_param_list = second_encryption_param_list[-1].split('&')
    obfs_param = base64decode(encryption_param_list[0].split('=')[-1])
    protocol_param = base64decode(encryption_param_list[1].split('=')[-1])
    remarks = base64decode(encryption_param_list[2].split('=')[-1])
    group = base64decode(encryption_param_list[3].split('=')[-1])
    ssr_dict = dict()
    ssr_dict['server'] = server
    ssr_dict['server_port'] = int(port)
    ssr_dict['method'] = method
    ssr_dict['obfs'] = obfs
    ssr_dict['protocol'] = protocol
    ssr_dict['password'] = password
    ssr_dict['obfs_param'] = obfs_param
    ssr_dict['protocol_param'] = protocol_param
    ssr_dict['remarks'] = "".join(remarks.split("\t"))
    ssr_dict['group'] = group
    ssr_dict['ping'] = get_ping_speed(server, remarks)
    return ssr_dict

# 生成ssr 信息列表字典
def generate_ssr_info_dict_list(ssr_url_list):
    ssr_info_dict_list = list()
    for ssr_url in ssr_url_list:
        ssr_info_dict = analysis_ssr_url(ssr_url)
        ssr_info_dict_list.append(ssr_info_dict)
    return ssr_info_dict_list

# 生成打印表格
def generate_ssr_display_table(ssr_info_dict_list):
    table = DrawTable()
    id = 1
    for ssr_info_dict in ssr_info_dict_list:
        color = colored()
        if ssr_info_dict['ping'] == '∞':
            ping = color.red(ssr_info_dict['ping'])
        else:
            ping = color.green(str(ssr_info_dict['ping']))
        table.append(
            id = id,
            name=ssr_info_dict['remarks'],
            ping=ping,
            server=ssr_info_dict['server'],
            port=ssr_info_dict['server_port'],
            method=ssr_info_dict['method']
        )
        id = id + 1
    return table.str()

# 获取ssr节点ping值
def get_ping_speed(server, remarks):
    color = colored()
    ping_len = "8"
    cmd = "ping -c 4 %s |grep 'time=' | awk '{print $%s}' |cut -b 6-" % (server,ping_len)
    ping_speed = os.popen(cmd).readlines()
    if ping_speed:
        ping_speed = float(ping_speed[0].strip())
        flag = color.green("√")
    else:
        ping_speed = '∞'
        flag = color.red("×")
    print("Testing ping:", remarks, server, flag)
    return ping_speed

