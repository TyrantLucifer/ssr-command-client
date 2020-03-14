#!/usr/bin/env python3
# coding=utf-8

import argparse
from funtions import *

def get_parser():
    parser = argparse.ArgumentParser(description="The ssr commend client based Python.")
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
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.list:
        show_ssr_list()
    elif args.update:
        update_ssr_list_info()
    elif args.config and not args.port:
        generate_config_json(args.config)
    elif args.config and args.port:
        generate_config_json(args.config, args.port)
    elif args.fast_node and not args.port:
        id = serach_fast_node() + 1
        generate_config_json(id)
    elif args.fast_node and args.port:
        id = serach_fast_node() + 1
        generate_config_json(id, args.port)
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
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
