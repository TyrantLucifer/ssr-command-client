"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: main.py
@time: 2021/2/18 21:36
@desc: shadowsocksr-cli入口函数
"""

import argparse
from shadowsocksr_cli.functions import *


def get_parser():
    parser = argparse.ArgumentParser(description=color.blue("The shadowsocksr command client based Python."),
                                     epilog=color.yellow('Powered by ') + color.green('tyrantlucifer') + color.yellow(
                                         ". If you have any questions,you can send e-mails to ") + color.green(
                                         "tyrantlucifer@gmail.com"))
    parser.add_argument("-l", "--list", action="store_true", help="show ssr list")
    parser.add_argument("-p", "--port", default=1080, metavar="local_port", type=int,
                        help="assign local proxy port,use with -s")
    parser.add_argument("-s", "--start", metavar="ssr_id", type=int, help="start ssr proxy")
    parser.add_argument("-S", "--stop", nargs='?', const=1, metavar="ssr_id", type=int, help="stop ssr proxy")
    parser.add_argument("-u", "--update", action="store_true", help="update ssr list")
    parser.add_argument("-v", "--version", action="store_true", help="display version")
    parser.add_argument("--generate-clash", action="store_true", help="generate clash config yaml")
    parser.add_argument("--display-json", metavar="ssr_id", type=int, help="display ssr json info")
    parser.add_argument("--test-speed", type=int, metavar="ssr_id", help="test ssr nodes download and upload speed")
    parser.add_argument("--fast-node", action="store_true", help="find most fast by delay and start ssr proxy")
    parser.add_argument("--setting-url", metavar="ssr_subscribe_url", help="setting ssr subscribe url")
    parser.add_argument("--setting-address", metavar="ssr_local_address", help="setting ssr local address")
    parser.add_argument("--list-url", action="store_true", help="list ssr subscribe url")
    parser.add_argument("--add-url", metavar="ssr_subscribe_url", help="add ssr subscribe url")
    parser.add_argument("--remove-url", metavar="ssr_subscribe_url", help="remove ssr subscribe url")
    parser.add_argument("--list-address", action="store_true", help="list ssr local address")
    parser.add_argument("--parse-url", metavar="ssr_url", help="pares ssr url")
    parser.add_argument("--add-ssr", metavar="ssr_url", help="add ssr node")
    parser.add_argument("--test-again", metavar="ssr_node_id", type=int, help="test ssr node again")
    parser.add_argument("--print-qrcode", metavar="ssr_node_id", type=int, help="print ssr node qrcode")
    parser.add_argument("--setting-global-proxy", action="store_true",
                        help="setting system global proxy,only support on " + color.red('Ubuntu Desktop'))
    parser.add_argument("--setting-pac-proxy", action="store_true",
                        help="setting system pac proxy,only support on " + color.red('Ubuntu Desktop'))
    parser.add_argument("--close-system-proxy", action="store_true",
                        help="close system proxy,only support on " + color.red('Ubuntu Desktop'))
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.list:
        DisplayShadowsocksr.display_shadowsocksr_list()
    elif args.update:
        UpdateConfigurations.update_subscribe()
    elif args.fast_node:
        HandleShadowsocksr.select_fast_node(args.port)
    elif args.start is not None:
        HandleShadowsocksr.start(ssr_id=args.start, local_port=args.port)
    elif args.stop:
        HandleShadowsocksr.stop(ssr_id=args.stop, local_port=args.port)
    elif args.version:
        DisplayShadowsocksr.display_version()
    elif args.setting_url:
        UpdateConfigurations.reset_subscribe_url(args.setting_url)
    elif args.setting_address:
        UpdateConfigurations.update_local_address(args.setting_address)
    elif args.list_url:
        DisplayShadowsocksr.display_subscribe_url()
    elif args.add_url:
        UpdateConfigurations.add_subscribe_url(args.add_url)
    elif args.remove_url:
        UpdateConfigurations.remove_subscribe_url(args.remove_url)
    elif args.list_address:
        DisplayShadowsocksr.display_local_address()
    elif args.parse_url:
        DisplayShadowsocksr.display_shadowsocksr_json_by_url(args.parse_url)
    elif args.add_ssr:
        UpdateConfigurations.add_shadowsocksr_by_url(args.add_ssr)
    elif args.test_again is not None:
        UpdateConfigurations.update_shadowsocksr_connect_status(ssr_id=args.test_again)
    elif args.print_qrcode is not None:
        DisplayShadowsocksr.display_qrcode(ssr_id=args.print_qrcode)
    elif args.setting_global_proxy:
        UpdateSystemProxy.open_global_proxy(args.port)
    elif args.setting_pac_proxy:
        UpdateSystemProxy.open_pac_proxy()
    elif args.close_system_proxy:
        UpdateSystemProxy.close_proxy()
    elif args.test_speed is not None:
        DisplayShadowsocksr.display_shadowsocksr_speed(ssr_id=args.test_speed)
    elif args.display_json is not None:
        DisplayShadowsocksr.display_shadowsocksr_json(ssr_id=args.display_json)
    elif args.generate_clash:
        GenerateClashConfig.generate_clash_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
