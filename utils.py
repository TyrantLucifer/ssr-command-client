#!/usr/bin/env python3
# coding=utf-8

# 导入相关系统包
import requests
import base64
import zipfile
import configparser
import socket
import ping3
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
            "port_status",
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
                kwargs['port_status'],
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
    result = requests.get(url, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3742.400 QQBrowser/10.5.3864.400'})
    try:
        ssr_result = base64decode(result.text)
    except:
        print(color.red("ssr subscribe url parsed failed,please check the ssr subscribe url~~"))
        return None
    else:
        ssr_list = ssr_result.split('\n')
        ssr_real_list = list()
        for ssr in ssr_list:
            if ssr:
                ssr_real_list.append(ssr[6:])
        return ssr_real_list

# 解析ssr url链接
def analysis_ssr_url(ssr_url):
    try:
        ssr_url = base64decode(ssr_url)
    except:
        pass
    else:
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
        ssr_dict['port_status'] = get_port_status(server, int(port))
        return ssr_dict

# 生成ssr 信息列表字典
def generate_ssr_info_dict_list(ssr_url_list):
    ssr_info_dict_list = list()
    for ssr_url in ssr_url_list:
        ssr_info_dict = analysis_ssr_url(ssr_url)
        if ssr_info_dict: 
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
        if ssr_info_dict['port_status'] == "×":
            port_status = color.red(ssr_info_dict['port_status'])
        else:
            port_status = color.green(ssr_info_dict['port_status'])

        table.append(
            id = id,
            name=ssr_info_dict['remarks'],
            ping=ping,
            port_status=port_status,
            server=ssr_info_dict['server'],
            port=ssr_info_dict['server_port'],
            method=ssr_info_dict['method']
        )
        id = id + 1
    return table.str()

# 获取ssr节点ping值
def get_ping_speed(server, remarks):
    color = colored()
    ping_speed = ping3.ping(server, timeout=3, unit='ms')
    if ping_speed:
        flag = color.green('√')
        ping_speed = format(ping_speed, '.3f')
    else:
        flag = color.red('×')
        ping_speed = '∞'
    print("Testing ping:", remarks, server, flag)
    return ping_speed

# 获取用户家目录
def get_home_dir():
    cmd = 'echo ${HOME}'
    home_dir = os.popen(cmd).read().strip()
    return home_dir

# 获取配置目录
def get_config_dir():
    home_dir = get_home_dir()
    config_dir = os.path.join(home_dir, '.ssr-command-client')
    config_file_dir = os.path.join(config_dir, 'config.ini')
    lock_file_dir = os.path.join(config_dir, '.config.lock')
    return config_dir, config_file_dir, lock_file_dir

# 创建配置目录
def create_config_dir():
    config_dir, config_file_dir, lock_file_dir = get_config_dir()
    if os.path.exists(config_dir):
        pass
    else:
        os.mkdir(config_dir)
    if os.path.exists(config_file_dir):
        pass
    else:
        with open(config_file_dir, 'w') as file:
            file.write('')

# 下载ssr源码
def download_ssr_source():
    url = 'https://github.com/TyrantLucifer/shadowsocksr/archive/3.2.2.zip'
    result = requests.get(url, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3742.400 QQBrowser/10.5.3864.400'})
    config_dir, config_file_dir, lock_file_dir = get_config_dir()
    shadowsocksr_zip_file_path = os.path.join(config_dir, 'shadowsocksr.zip')
    with open(shadowsocksr_zip_file_path, "wb") as file:
        file.write(result.content)
    zipFile = zipfile.ZipFile(shadowsocksr_zip_file_path)
    zipFile.extractall(config_dir)
    os.chdir(config_dir)
    os.rename(zipFile.namelist()[0], 'shadowsocksr')

# 初始化配置文件
def init_config_file():
    config_dir, config_file_dir, lock_file_dir = get_config_dir()
    server_json_file_path = os.path.join(config_dir, 'ssr-list.json')
    config_json_file_path = os.path.join(config_dir, 'config.json')
    shadowsocksr_client_path = os.path.join(config_dir, 'shadowsocksr/shadowsocks/local.py')
    shadowsocksr_pid_file_path = os.path.join(config_dir, 'shadowsocksr.pid')
    shadowsocksr_log_file_path = os.path.join(config_dir, 'shadowsocksr.log')
    cf = configparser.ConfigParser()
    cf.add_section('default')
    cf.set('default', 'subscribe_url', 'https://raw.githubusercontent.com/satrom/V2SSR/master/SSR/Day.txt')
    cf.set('default', 'server_json_file_path', server_json_file_path)
    cf.set('default', 'config_json_file_path', config_json_file_path)
    cf.set('default', 'local_address', '127.0.0.1')
    cf.set('default', 'timeout', '300')
    cf.set('default', 'workers', '1')
    cf.set('default', 'shadowsocksr_client_path', shadowsocksr_client_path)
    cf.set('default', 'shadowsocksr_pid_file_path', shadowsocksr_pid_file_path)
    cf.set('default', 'shadowsocksr_log_file_path', shadowsocksr_log_file_path)
    with open(config_file_dir, 'w+') as file:
        cf.write(file)
    with open(lock_file_dir, 'w') as lock_file:
        lock_file.write('')

# 获取配置项
def get_config_value(key):
    config_dir, config_file_dir, lock_file_dir = get_config_dir()
    cf = configparser.ConfigParser()
    cf.read(config_file_dir)
    return cf.get('default', key)

# 设置配置项
def set_config_value(key, value):
    config_dir, config_file_dir, lock_file_dir = get_config_dir()
    cf = configparser.ConfigParser()
    cf.read(config_file_dir)
    cf.set('default', key, str(value))
    with open(config_file_dir, 'w+') as file:
        cf.write(file)

# 测试端口是否可以联通
def get_port_status(server, port):
    server_addr = (server, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(server_addr)
    except:
        flag = "×"
    else:
        flag = "√"
    s.close()
    return flag
