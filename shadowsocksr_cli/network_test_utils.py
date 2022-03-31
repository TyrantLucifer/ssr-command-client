"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: network_test_utils.py
@time: 2021/2/18 22:08
@desc: 提供测试shadowsocksr连接延迟，tcp端口状态，上传下载速度工具类
"""
import requests
import socks
import socket
from shadowsocksr_cli import speedtest
from multiprocessing import Pool, Process, freeze_support, get_context
from shadowsocksr_cli.handle_utils import *
from shadowsocksr_cli.setting_utils import *


class ShadowsocksrTest(object):
    """提供shadowsocksr节点测速功能工具类

    为Function提供测速功能

    属性:
        None
    """

    def __init__(self):
        pass

    @staticmethod
    def is_valid_connect(server, port):
        """测试服务器和端口和本地是否连通

        :param server: 服务器地址
        :param port:  服务器tcp端口
        :return: connect: True or False,表示是否可以连接
                 delay: 本地到目标服务器tcp连接延迟
        """
        server_addr = (server, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        start_time = time.time()
        try:
            s.connect(server_addr)
            end_time = time.time()
        except Exception as e:
            logger.debug(e)
            logger.debug('Server: {0}  Port: {1} is invalid'.format(server, port))
            s.close()
            return False, '∞'
        else:
            delay = round(end_time - start_time, 2) * 1000
            return True, str(delay)

    @staticmethod
    def test_shadowsocksr_connect(ssr_dict):
        connect, ping = ShadowsocksrTest.is_valid_connect(ssr_dict['server'],
                                                          int(ssr_dict['server_port']))
        ssr_dict['ping'] = ping
        ssr_dict['connect'] = connect
        return ssr_dict

    @staticmethod
    def connect_thread_pool(ssr_dict_list):
        freeze_support()
        thread_list = list()
        result_list = list()
        if 'ARM' in init_config.system:
            pool = get_context("fork").Pool(50)
        else:
            pool = Pool(50)
        for ssr_dict in ssr_dict_list:
            thread = pool.apply_async(ShadowsocksrTest.test_shadowsocksr_connect,
                                      args=(ssr_dict,))
            thread_list.append(thread)
        pool.close()
        pool.join()
        for thread in thread_list:
            ssr_dict = thread.get()
            result_list.append(ssr_dict)
        return result_list

    @staticmethod
    @calculate
    def test_shadowsocksr_speed(ssr_dict, local_port=60000):
        kwargs = {
            'local_address': '127.0.0.1',
            'local_port': local_port,
            'timeout': int(Setting.get_value('timeout')),
            'workers': int(Setting.get_value('workers'))
        }
        if ssr_dict['connect']:
            p = Process(target=ControlShadowsocksr.start_on_windows,
                        args=(ssr_dict,),
                        kwargs=kwargs)
            p.daemon = True
            p.start()
            socks.set_default_proxy(socks.SOCKS5,
                                    kwargs['local_address'],
                                    kwargs['local_port'])
            socket.socket = socks.socksocket
            try:
                s = speedtest.Speedtest()
                s.upload(pre_allocate=False)
                s.download()
            except Exception as e:
                logger.debug(e)
                logger.debug("This ssr node is invalid")
                download = '∞'
                upload = '∞'
            else:
                result = s.results.dict()
                download = round(result['download'] / 1000.0 / 1000.0, 2)
                upload = round(result['upload'] / 1000.0 / 1000.0, 2)
            ssr_dict['download'] = download
            ssr_dict['upload'] = upload
        else:
            ssr_dict['download'] = '∞'
            ssr_dict['upload'] = '∞'
        logger.info("Shadowsocksr - name: {0}".format(ssr_dict['remarks']))
        logger.info("Download: {0} MB/s".format(ssr_dict['download']))
        logger.info("Upload: {0} MB/s".format(ssr_dict['upload']))
        return ssr_dict

    @staticmethod
    @calculate
    def test_shadowsocksr_netflix(ssr_dict, local_port=60000):
        kwargs = {
            'local_address': '127.0.0.1',
            'local_port': local_port,
            'timeout': int(Setting.get_value('timeout')),
            'workers': int(Setting.get_value('workers'))
        }
        if ssr_dict['connect']:
            p = Process(target=ControlShadowsocksr.start_on_windows,
                        args=(ssr_dict,),
                        kwargs=kwargs)
            p.daemon = True
            p.start()
            socks.set_default_proxy(socks.SOCKS5,
                                    kwargs['local_address'],
                                    kwargs['local_port'])
            socket.socket = socks.socksocket
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
            }
            self_made = "https://www.netflix.com/title/70242311"
            other_made = "https://www.netflix.com/title/70143836"
            try:
                r1 = requests.get(self_made, headers=headers, timeout=20)
                r2 = requests.get(other_made, headers=headers, timeout=20)
                if r1.status_code == 200 and r2.status_code == 200:
                    logger.info("Shadowsocksr - name: {0} Full native".format(ssr_dict['remarks']))
                elif r1.status_code == 200:
                    logger.info("Shadowsocksr - name: {0} Only original".format(ssr_dict['remarks']))
                else:
                    logger.info("Shadowsocksr - name: {0} Can not unlock netflix".format(ssr_dict['remarks']))
            except Exception as e:
                logger.error(e)
        else:
            logger.info("Shadowsocksr - name: {0} is invalid".format(ssr_dict['remarks']))
