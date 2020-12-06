'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午7:24
'''

import logging

logger = logging.getLogger("ssr-command-client")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
