'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午7:24
'''

import logging
import datetime

def calculate(func):
    def main(*args):
        start = datetime.datetime.now()
        content = func(*args)
        end = datetime.datetime.now()
        logger.info("Func - {0} Total time: {1}s".format(func.__name__, (end - start).microseconds / 1000000))
        return content
    return main

logger = logging.getLogger("ssr-command-client")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - [%(funcName)s] - %(levelname)s: %(message)s')
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

ssrLogger = logging.getLogger("shadowsocksr")
ssrLogger.setLevel(logging.INFO)