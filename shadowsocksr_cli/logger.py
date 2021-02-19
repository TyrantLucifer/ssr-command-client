"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: logger.py
@time: 2021/2/18 19:59
@desc: 初始化全局log变量
"""

import logging
import time

from shadowsocksr_cli.init_utils import *

# 初始化工具类init_utils.InitConfig
init_config = InitConfig()

# 初始化全局logger记录格式及级别
logger = logging.getLogger("shadowsocksr-cli")
logger.setLevel(logging.DEBUG)

# 初始化全局logger控制台终端记录格式及级别
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - [%(funcName)s] - %(levelname)s: %('
                              'message)s')
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 初始化全局logger文件记录格式及级别
log_file_handler = logging.FileHandler(init_config.log_file)
log_file_handler.setLevel(logging.DEBUG)
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)

# 初始化全局ssr_logger记录格式及级别
ssr_logger = logging.getLogger("shadowsocksr")
ssr_logger.setLevel(logging.INFO)

# 初始化全局ssr_logger文件记录格式及级别
debug_file_handler = logging.FileHandler(init_config.debug_log_file)
debug_file_handler.setLevel(logging.ERROR)
debug_file_handler.setFormatter(formatter)
ssr_logger.addHandler(debug_file_handler)


# 定义计算函数运行时间装饰器
def calculate(func):
    def main(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        logger.info("Func - {0} Total time: {1}s".format(func.__name__,
                                                         round(time.time() - start, 2)))
    return main


# 定义判断操作系统是否为Ubuntu的装饰器
def is_ubuntu(func):
    def judge(*args, **kwargs):
        if init_config.system != 'Ubuntu':
            logger.info("Current OS - {0} {1} only support Ubuntu".format(init_config.system, func.__name__))
            sys.exit(1)
        else:
            func(*args, **kwargs)

    return judge


# 定义判断shadowsocksr id是否合法装饰器
def is_id_valid(ssr_dict_list):
    def wrapper(func):
        def judge(*args, **kwargs):
            if kwargs['ssr_id'] < 0 or kwargs['ssr_id'] >= len(ssr_dict_list):
                logger.error('Shadowsocksr id error')
                sys.exit(1)
            else:
                ssr_logger.addHandler(stream_handler)
                func(*args, **kwargs)
                ssr_logger.removeHandler(stream_handler)

        return judge

    return wrapper
