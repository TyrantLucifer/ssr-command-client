#!/usr/bin/env python3
# coding=utf-8
import json
from utils import *
from conf import *

def generate_config_json(id, port=1080):
    if os.path.exists(SERVER_JSON_FILE_PATH):
        with open(SERVER_JSON_FILE_PATH, 'r') as file:
            json_str = file.read()
        ssr_info_dict_list = json.loads(json_str)
    else:
        ssr_info_dict_list = update_ssr_list_info()
    ssr_info_dict = ssr_info_dict_list[id - 1]
    ssr_info_dict['local_address'] = LOCAL_ADDRESS 
    ssr_info_dict['timeout'] = TIMEOUT
    ssr_info_dict['workers'] = WORKERS
    ssr_info_dict['local_port'] = port
    ssr_info = json.dumps(ssr_info_dict)
    with open(CONFIG_JSON_FILE_PATH, 'w') as file:
        file.write(ssr_info)
    print('config json file is update~~')


def update_ssr_list_info():
    ssr_url_list = get_ssr_list(SUBSCRIBE_URL)
    ssr_info_dict_list = generate_ssr_info_dict_list(ssr_url_list)
    json_str = json.dumps(ssr_info_dict_list)
    with open(SERVER_JSON_FILE_PATH, 'w') as file:
        file.write(json_str)
    print('SSR list is update~~')
    return ssr_info_dict_list

def show_ssr_list():
    if os.path.exists(SERVER_JSON_FILE_PATH):
        with open(SERVER_JSON_FILE_PATH, 'r') as file:
            json_str = file.read()
        ssr_info_dict_list = json.loads(json_str)
    else:
        ssr_info_dict_list = update_ssr_list_info()
    table = generate_ssr_display_table(ssr_info_dict_list)
    print(table)

def start_ssr_proxy():
    if os.path.exists(CONFIG_JSON_FILE_PATH):
        if os.path.exists('/var/run/shadowsocksr.pid'):
            print('Proxy is already start~~')
        else:
            cmd = '{0} -c {1} -d start'.format(SHADOWSOCKR_CLIENT_PATH,
                                              CONFIG_JSON_FILE_PATH)
            os.system(cmd)
            print('Proxy is start~~')
    else:
        print("Config json file is not exists,Please use the option -c to create config json file~~")

def stop_ssr_proxy():
    if os.path.exists(CONFIG_JSON_FILE_PATH):
        if os.path.exists('/var/run/shadowsocksr.pid'):
            cmd = '{0} -c {1} -d stop'.format(SHADOWSOCKR_CLIENT_PATH,
                                                  CONFIG_JSON_FILE_PATH)
            os.system(cmd)
            print('Proxy is stop~~')
        else:
            print('Proxy is already stop~~')
    else:
        print("Config json file is not exists,Please use the option -c to create config json file~~")

