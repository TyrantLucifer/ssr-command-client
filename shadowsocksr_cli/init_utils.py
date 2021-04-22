"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: init_utils.py
@time: 2021/2/18 10:31
@desc: 初始化工具类集合
"""

import os
import sys
import platform
import configparser


class InitConfig(object):
    """初始化工具类

    当shadowsocksr-cli启动时初始化相关属性

    属性:
        version: 版本号
        platform: 操作系统平台
        system: 操作系统
        home_dir: 家目录路径
        config_dir: 配置目录路径
        config_file: 配置文件
        config_lock_file: 配置锁文件
        pid_file: shadowsocksr代理启动pid文件
        log_file: shadowsocksr-cli日志记录文件
        debug_log_file: shadowsocksr debug日志文件
        ssr_list_json: shadowsocksr节点列表详细信息文件
        ssr_json: shadowsocksr节点json文件
        pac_file: pac代理文件
        clash_config_file: clash配置文件
        subscribe_url: shadowsocksr订阅链接
        local_address: shadowsocksr本地监听地址
        timeout: shadowsocksr客户端延迟
        workers: shadowsocksr客户端加密强度
    """

    def __init__(self):
        self.version = '2.1.2'
        self.platform = sys.platform
        self.system = platform.system()
        self.home_dir = os.path.expanduser('~')
        self.config_dir = os.path.join(self.home_dir,
                                       '.ssr-command-client')
        self.config_file = os.path.join(self.config_dir,
                                        'config.ini')
        self.config_lock_file = os.path.join(self.config_dir,
                                             '.config.lock')
        self.pid_file = os.path.join(self.config_dir,
                                     'shadowsocksr.pid')
        self.log_file = os.path.join(self.config_dir,
                                     'shadowsocksr.log')
        self.debug_log_file = os.path.join(self.config_dir,
                                           'shadowsocksrDebug.log')
        self.ssr_list_json = os.path.join(self.config_dir,
                                          'ssr-list.json')
        self.ssr_json = os.path.join(self.config_dir,
                                     'config.json')
        self.pac_file = os.path.join(self.config_dir,
                                     'autoProxy.pac')
        self.clash_config_file = os.path.join(self.config_dir,
                                              'clashConfig.yaml')
        self.http_server_pid_file = os.path.join(self.config_dir,
                                                 'httpd.pid')
        self.http_log_file = os.path.join(self.config_dir,
                                          'httpd.log')
        self.http_error_log_file = os.path.join(self.config_dir,
                                                'httpd_error.log')
        self.subscribe_url = 'https://tyrantlucifer.com/ssr/ssr.txt'
        self.local_address = '127.0.0.1'
        self.timeout = 300
        self.workers = 1

        if not self.__is_exist_config_dir():
            self.__create_config_dir()

    def __is_exist_config_dir(self):
        if os.path.exists(self.config_dir):
            return True
        else:
            return False

    def __initConfigFile(self):
        config = configparser.ConfigParser()
        config.add_section('default')
        config.set('default', 'subscribe_url', self.subscribe_url)
        config.set('default', 'server_json_file_path', self.ssr_list_json)
        config.set('default', 'config_json_file_path', self.ssr_json)
        config.set('default', 'local_address', self.local_address)
        config.set('default', 'timeout', str(self.timeout))
        config.set('default', 'workers', str(self.workers))
        config.set('default', 'shadowsocksr_pid_file_path', self.pid_file)
        config.set('default', 'shadowsocksr_log_file_path', self.log_file)
        with open(self.config_file, 'w+') as file:
            config.write(file)
        with open(self.config_lock_file, 'w') as lock_file:
            lock_file.write('')

    def __create_config_dir(self):
        os.mkdir(self.config_dir)
        with open(self.config_file, 'w') as file:
            file.write('')
        self.__initConfigFile()
