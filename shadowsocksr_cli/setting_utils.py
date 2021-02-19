"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: setting_utils.py
@time: 2021/2/18 22:42
@desc:
"""

from shadowsocksr_cli.logger import *


class Setting(object):
    """配置项工具类

    提供从本地配置文件中读取对应参数的功能

    属性:
        config: 配置文件对象
    """
    config = configparser.ConfigParser()
    config.read(init_config.config_file)

    def __init__(self):
        pass

    @staticmethod
    def get_value(key):
        return Setting.config.get('default', key)

    @staticmethod
    def set_value(key, value):
        Setting.config.set('default', key, str(value))
        with open(init_config.config_file, 'w+') as file:
            Setting.config.write(file)

