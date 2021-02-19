"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: update_utils.py
@time: 2021/2/18 21:13
@desc: 提供shadowsocksr订阅更新功能工具类
"""

import json
from shadowsocksr_cli.parse_utils import *
from shadowsocksr_cli.network_test_utils import *


class UpdateShadowsocksr(object):
    """更新shadowsocksr节点信息工具类

    为shadowsocksr-cli功能提供更新shadowsocksr节点的工具类

    属性:
        subscribe_url_list: shadowsocksr 订阅链接列表
        ssr_dict_list: shadowsocksr节点信息字典列表
    """

    def __init__(self):
        self.subscribe_url_list = Setting.get_value("subscribe_url").split('|')
        self.ssr_dict_list = list()
        self.get_all_shadowsocksr_info()

    @calculate
    def update(self):
        self.ssr_dict_list.clear()
        for subscribe_url in self.subscribe_url_list:
            ssr_dict_list = ParseShadowsocksr.parse_shadowsocksr_by_subscribe_url(subscribe_url)
            self.ssr_dict_list = self.ssr_dict_list + ssr_dict_list

        for i in range(len(self.ssr_dict_list)):
            self.ssr_dict_list[i]['id'] = i
            # self.ssr_dict_list[i] = ShadowsocksrTest.test_shadowsocksr_connect(ssr_dict_list[i])

        self.ssr_dict_list = ShadowsocksrTest.connect_thread_pool(self.ssr_dict_list)
        self.update_cache_json()

    def get_all_shadowsocksr_info(self):
        if os.path.exists(init_config.ssr_list_json):
            with open(init_config.ssr_list_json, 'r', encoding='utf-8') as file:
                content = file.read()
                self.ssr_dict_list = json.loads(content)
        else:
            self.update()

    def add_shadowsocksr_by_url(self, ssr_url):
        ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
        ssr_dict = ShadowsocksrTest.test_shadowsocksr_connect(ssr_dict)
        ssr_dict['id'] = len(self.ssr_dict_list)
        self.ssr_dict_list.append(ssr_dict)
        self.update_cache_json()

    def update_cache_json(self):
        with open(init_config.ssr_list_json, 'w', encoding='utf-8') as file:
            content = json.dumps(self.ssr_dict_list, ensure_ascii=False, indent=4)
            file.write(content)
