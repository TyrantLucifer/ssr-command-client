"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: handle_utils.py
@time: 2021/2/19 16:28
@desc: 提供shadowsocksr节点控制功能工具类
"""

import signal
from shadowsocksr_cli.shadowsocks import daemon, eventloop, tcprelay, udprelay, asyncdns
from shadowsocksr_cli.logger import *


class ControlShadowsocksr(object):
    """控制shadowsocksr节点启停工具类

    提供shadowsocksr代理启动功能

    属性:
        None
    """

    def __init__(self):
        pass

    @staticmethod
    def start_on_windows(ssr_dict, **kwargs):
        """在Windows操作系统平台开启shadowsocksr代理

        :param kwargs:
            local_address: 本地监听地址
            local_port: 本地监听端口
            timeout: 启动延迟
            workers: 加密级别
        :type ssr_dict: shadowsocksr节点信息字典

        """
        ssr_dict['local_address'] = kwargs['local_address']
        ssr_dict['local_port'] = kwargs['local_port']
        ssr_dict['timeout'] = kwargs['timeout']
        ssr_dict['workers'] = kwargs['workers']

        if not ssr_dict.get('dns_ipv6', False):
            asyncdns.IPV6_CONNECTION_SUPPORT = False
        try:
            daemon.daemon_exec(ssr_dict)
            dns_resolver = asyncdns.DNSResolver()
            tcp_server = tcprelay.TCPRelay(ssr_dict, dns_resolver, True)
            udp_server = udprelay.UDPRelay(ssr_dict, dns_resolver, True)
            loop = eventloop.EventLoop()
            dns_resolver.add_to_loop(loop)
            tcp_server.add_to_loop(loop)
            udp_server.add_to_loop(loop)

            def handler(signum, _):
                logger.info('received SIGQUIT, doing graceful shutting down..')
                tcp_server.close(next_tick=True)
                udp_server.close(next_tick=True)

            signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

            def int_handler(signum, _):
                logger.info("Shadowsocksr is stop")
                sys.exit(1)

            signal.signal(signal.SIGINT, int_handler)
            daemon.set_user(ssr_dict.get('user', None))
            logger.info('Shadowsocksr is start on {0}:{1}'.format(kwargs['local_address'], kwargs['local_port']))
            logger.info('Press Ctrl+C to stop shadowsocksr')
            loop.run()
        except Exception as e:
            logger.error(e)
            sys.exit(1)

    @staticmethod
    def operate_on_unix(ssr_dict, **kwargs):
        """在Unix操作系统平台开启shadowsocksr代理

        :param kwargs:
            local_address: 本地监听地址
            local_port: 本地监听端口
            timeout: 启动延迟
            workers: 加密级别
            pid_file: shadowsocksr进程号文件
            log_file: shadowsocksr日志文件
            daemon: 标识操作，启动或者停止
        :type ssr_dict: shadowsocksr节点信息字典

        """
        ssr_dict['daemon'] = kwargs['daemon']
        ssr_dict['local_address'] = kwargs['local_address']
        ssr_dict['local_port'] = kwargs['local_port']
        ssr_dict['timeout'] = kwargs['timeout']
        ssr_dict['workers'] = kwargs['workers']
        ssr_dict['pid-file'] = kwargs['pid_file']
        ssr_dict['log-file'] = kwargs['log_file']

        if not ssr_dict.get('dns_ipv6', False):
            asyncdns.IPV6_CONNECTION_SUPPORT = False
        try:
            daemon.daemon_exec(ssr_dict)
            dns_resolver = asyncdns.DNSResolver()
            tcp_server = tcprelay.TCPRelay(ssr_dict, dns_resolver, True)
            udp_server = udprelay.UDPRelay(ssr_dict, dns_resolver, True)
            loop = eventloop.EventLoop()
            dns_resolver.add_to_loop(loop)
            tcp_server.add_to_loop(loop)
            udp_server.add_to_loop(loop)

            def handler(signum, _):
                logger.info('received SIGQUIT, doing graceful shutting down..')
                tcp_server.close(next_tick=True)
                udp_server.close(next_tick=True)

            signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

            def int_handler(signum, _):
                logger.info("Shadowsocksr is stop")
                sys.exit(1)

            signal.signal(signal.SIGINT, int_handler)
            daemon.set_user(ssr_dict.get('user', None))
            logger.info('Shadowsocksr is start on {0}:{1}'.format(kwargs['local_address'], kwargs['local_port']))
            loop.run()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
