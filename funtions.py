#!/usr/bin/env python3
# coding=utf-8
import json
from utils import *
from conf import *

config_dir, config_file_dir, lock_file_dir = get_config_dir()
if os.path.exists(lock_file_dir):
    SUBSCRIBE_URL = get_config_value('SUBSCRIBE_URL')
    SERVER_JSON_FILE_PATH = get_config_value('SERVER_JSON_FILE_PATH')
    CONFIG_JSON_FILE_PATH = get_config_value('CONFIG_JSON_FILE_PATH')
    LOCAL_ADDRESS = get_config_value('LOCAL_ADDRESS')
    SHADOWSOCKSR_CLIENT_PATH = get_config_value('SHADOWSOCKSR_CLIENT_PATH')
    TIMEOUT = int(get_config_value('TIMEOUT'))
    WORKERS = int(get_config_value('WORKERS'))
    SHADOWSOCKSR_PID_FILE_PATH = get_config_value('SHADOWSOCKSR_PID_FILE_PATH')
else:
    create_config_dir()
    download_ssr_source()
    init_config_file()
    SUBSCRIBE_URL = get_config_value('SUBSCRIBE_URL')
    SERVER_JSON_FILE_PATH = get_config_value('SERVER_JSON_FILE_PATH')
    CONFIG_JSON_FILE_PATH = get_config_value('CONFIG_JSON_FILE_PATH')
    LOCAL_ADDRESS = get_config_value('LOCAL_ADDRESS')
    SHADOWSOCKR_CLIENT_PATH = get_config_value('SHADOWSOCKSR_CLIENT_PATH')
    TIMEOUT = int(get_config_value('TIMEOUT'))
    WORKERS = int(get_config_value('WORKERS'))
    SHADOWSOCKR_PID_FILE_PATH = get_config_value('SHADOWSOCKR_PID_FILE_PATH')
    
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
        if os.path.exists(SHADOWSOCKSR_PID_FILE_PATH):
            print('Proxy is already start~~')
        else:
            cmd = 'python3 {0} -c {1} -d start --pid-file {2}'.format(SHADOWSOCKSR_CLIENT_PATH,
                                              CONFIG_JSON_FILE_PATH, SHADOWSOCKSR_PID_FILE_PATH)
            os.system(cmd)
            print('Proxy is start~~')
    else:
        print("Config json file is not exists,Please use the option -c to create config json file~~")

def stop_ssr_proxy():
    if os.path.exists(CONFIG_JSON_FILE_PATH):
        if os.path.exists(SHADOWSOCKSR_PID_FILE_PATH):
            cmd = 'python3 {0} -c {1} -d stop --pid-file {2}'.format(SHADOWSOCKSR_CLIENT_PATH,
                                                  CONFIG_JSON_FILE_PATH, SHADOWSOCKSR_PID_FILE_PATH)
            os.system(cmd)
            print('Proxy is stop~~')
        else:
            print('Proxy is already stop~~')
    else:
        print("Config json file is not exists,Please use the option -c to create config json file~~")

def display_version():
    color = colored()
    version = color.yellow("ssr-command-client v1.0")
    author = color.blue("Powered by TyrantLucifer~~")
    print(version)
    print(author)





