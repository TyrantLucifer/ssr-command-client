#!/usr/bin/env python3
# coding=utf-8

import argparse
from funtions import *

def get_parser():
    parser = argparse.ArgumentParser(description="The ssr commend client based Python.")
    parser.add_argument("-l", "--list", action="store_true", help="show ssr list")
    parser.add_argument("-p", "--port", default=1080, type=int, help="assign local proxy port,use with -c")
    parser.add_argument("-s", "--start", action="store_true", help="start ssr proxy")
    parser.add_argument("-S", "--stop", action="store_true", help="stop ssr proxy")
    parser.add_argument("-u", "--update", action="store_true", help="update ssr list")
    parser.add_argument("-c", "--config", metavar="ssr_node_id", type=int, help="generate ssr config json")
    parser.add_argument("-v", "--version", action="store_true", help="display version")
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
    elif args.start:
        start_ssr_proxy()
    elif args.stop:
        stop_ssr_proxy()
    elif args.version:
        display_version()
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
