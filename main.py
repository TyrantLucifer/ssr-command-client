#!/usr/bin/env python3
# coding=utf-8

import argparse
from funtions import *

def get_parser():
    parser = argparse.ArgumentParser(description="The ssr command client based Python.")
    parser.add_argument("-l", "--list", action="store_true", help="show ssr list")
    parser.add_argument("-p", "--port", default=1080, metavar="local_port", type=int, help="assign local proxy port,use with -c or --fast-node")
    parser.add_argument("-s", "--start", action="store_true", help="start ssr proxy")
    parser.add_argument("-S", "--stop", action="store_true", help="stop ssr proxy")
    parser.add_argument("-u", "--update", action="store_true", help="update ssr list")
    parser.add_argument("-c", "--config", metavar="ssr_node_id", type=int, help="generate ssr config json")
    parser.add_argument("-v", "--version", action="store_true", help="display version")
    parser.add_argument("--fast-node", action="store_true", help="generate fast ssr config json")
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
    parser.add_argument("--setting-global-proxy", action="store_true", help="setting system global proxy,only support Ubuntu Desktop")
    parser.add_argument("--setting-pac-proxy", action="store_true", help="setting system pac proxy,only support Ubuntu Desktop")
    parser.add_argument("--close-system-proxy", action="store_true", help="close system proxy,only support Ubuntu Desktop")
    parser.add_argument("--setting-auto-start", action="store_true", help="setting ssr auto start")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.list:
        show_ssr_list()
    elif args.update:
        update_ssr_list_info()
    elif args.config:
        generate_config_json(args.config, args.port)
    elif args.fast_node:
        node_id = serach_fast_node() + 1
        generate_config_json(node_id, args.port)
    elif args.start:
        start_ssr_proxy()
    elif args.stop:
        stop_ssr_proxy()
    elif args.version:
        display_version()
    elif args.setting_url:
        set_config_value('SUBSCRIBE_URL', args.setting_url)
    elif args.setting_address:
        set_config_value('LOCAL_ADDRESS', args.setting_address)
    elif args.list_url:
        display_ssr_subcribe_url()
    elif args.add_url:
        add_ssr_subcribe_url(args.add_url)
    elif args.remove_url:
        remove_ssr_subcribe_url(args.remove_url)
    elif args.list_address:
        print(LOCAL_ADDRESS)
    elif args.parse_url:
        parse_ssr_url(args.parse_url)
    elif args.add_ssr:
        add_ssr_node(args.add_ssr)
    elif args.test_again:
        test_node_again(args.test_again)
    elif args.print_qrcode:
        print_ssr_qrcode(args.print_qrcode)
    elif args.setting_global_proxy:
        open_global_proxy()
    elif args.setting_pac_proxy:
        open_pac_proxy()
    elif args.close_system_proxy:
        close_system_proxy()
    elif args.setting_auto_start:
        setting_auto_start()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
