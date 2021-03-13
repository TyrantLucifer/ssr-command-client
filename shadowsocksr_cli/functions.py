"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: functions.py
@time: 2021/2/18 21:37
@desc:
"""

import yaml
from shadowsocksr_cli.common import *


class DisplayShadowsocksr(object):
    """终端输出shadowsocksr节点信息工具类

    为main模块提供展示shadowsocksr节点列表功能，展示shadowsocksr节点测试速度功能

    属性:
        display_shadowsocksr_list: 打印shadowsocksr节点列表
        display_subscribe_url: 打印订阅链接
        display_local_address: 打印本地监听地址
        display_shadowsocksr_json: 打印shadowsocksr节点信息json
        display_qrcode: 打印shadowsocksr节点二维码
    """

    def __init__(self):
        pass

    @staticmethod
    def display_shadowsocksr_list():
        for ssr_dict in update_shadowsocksr.ssr_dict_list:
            if ssr_dict['connect']:
                delay = color.green(ssr_dict['ping'])
                connect = color.green('√')
            else:
                delay = color.red(ssr_dict['ping'])
                connect = color.red('×')

            ssr_list_table.append(
                id=ssr_dict['id'],
                name=ssr_dict['remarks'],
                delay=delay,
                connect=connect,
                server=ssr_dict['server'],
                port=ssr_dict['server_port'],
                method=ssr_dict['method']
            )
        ssr_list_table.print()

    @staticmethod
    def display_subscribe_url():
        for subscribe_url in update_shadowsocksr.subscribe_url_list:
            color.print(subscribe_url, 'blue')

    @staticmethod
    def display_local_address():
        color.print(Setting.get_value("local_address"), 'blue')

    @staticmethod
    @is_id_valid(update_shadowsocksr.ssr_dict_list)
    def display_shadowsocksr_json(ssr_id,
                                  ssr_dict_list=update_shadowsocksr.ssr_dict_list):
        color.print(json.dumps(ssr_dict_list[ssr_id],
                               ensure_ascii=False,
                               indent=4),
                    'yellow')

    @staticmethod
    def display_shadowsocksr_json_by_url(ssr_url):
        ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
        ssr_dict = ShadowsocksrTest.test_shadowsocksr_connect(ssr_dict)
        color.print(json.dumps(ssr_dict, ensure_ascii=False, indent=4),
                    'yellow')

    @staticmethod
    @is_id_valid(update_shadowsocksr.ssr_dict_list)
    def display_shadowsocksr_speed(ssr_id):
        ShadowsocksrTest.test_shadowsocksr_speed(update_shadowsocksr.ssr_dict_list[ssr_id])

    @staticmethod
    @is_id_valid(update_shadowsocksr.ssr_dict_list)
    def display_qrcode(ssr_id):
        PrintQrcode.print_qrcode(update_shadowsocksr.ssr_dict_list[ssr_id]['ssr_url'])

    @staticmethod
    def display_version():
        logger.info("Start get version from cloud, it will take a lot of time")
        result = requests.get('https://tyrantlucifer.com/ssr/version.json')
        result.encoding = 'utf-8'
        version = result.json()['version']
        tips_message = result.json()['tips_message']
        if version == init_config.version:
            logger.info("Current version {0} is newest. Please enjoy.".format(version))
        else:
            logger.info("Current version: {0}".format(init_config.version))
            logger.info("Newest version: {0}".format(version))
            logger.info("You can use 'pip(pip3) install shadowsocksr-cli' to update.")
        logger.info(tips_message)


class UpdateConfigurations(object):

    def __init__(self):
        pass

    @staticmethod
    def update_subscribe():
        update_shadowsocksr.update()

    @staticmethod
    def add_shadowsocksr_by_url(ssr_url):
        update_shadowsocksr.add_shadowsocksr_by_url(ssr_url)

    @staticmethod
    def reset_subscribe_url(subscribe_url):
        Setting.set_value('subscribe_url', subscribe_url)
        logger.info('Reset shadowsocksr subscribe url to: {0}'.format(subscribe_url))

    @staticmethod
    def update_local_address(local_address):
        Setting.set_value('local_address', local_address)
        logger.info('Update local address to: {0}'.format(local_address))

    @staticmethod
    def add_subscribe_url(subscribe_url):
        update_shadowsocksr.subscribe_url_list.append(subscribe_url)
        Setting.set_value('subscribe_url',
                          '|'.join(update_shadowsocksr.subscribe_url_list))
        logger.info('Add subscribe_url url: {0}'.format(subscribe_url))

    @staticmethod
    def remove_subscribe_url(subscribe_url):
        if subscribe_url in update_shadowsocksr.subscribe_url_list:
            update_shadowsocksr.subscribe_url_list.remove(subscribe_url)
            Setting.set_value('subscribe_url',
                              '|'.join(update_shadowsocksr.subscribe_url_list))
            logger.info("Remove subscribe url: {0}".format(subscribe_url))
        else:
            logger.error("Subscribe url: {0} is not existed".format(subscribe_url))

    @staticmethod
    @is_id_valid(update_shadowsocksr.ssr_dict_list)
    def update_shadowsocksr_connect_status(ssr_id):
        update_shadowsocksr.ssr_dict_list[ssr_id] = ShadowsocksrTest.test_shadowsocksr_connect(
            update_shadowsocksr.ssr_dict_list[ssr_id]
        )
        logger.info('Test node successfully, connect: {0} delay: {1}'.
                    format(update_shadowsocksr.ssr_dict_list[ssr_id]['connect'],
                           update_shadowsocksr.ssr_dict_list[ssr_id]['ping']))
        update_shadowsocksr.update_cache_json()


class HandleShadowsocksr(object):
    """控制shadowsocksr节点启停工具类

    """

    @staticmethod
    @is_id_valid(update_shadowsocksr.ssr_dict_list)
    def start(ssr_id, local_port):
        if init_config.platform == 'win32':
            ControlShadowsocksr.start_on_windows(update_shadowsocksr.ssr_dict_list[ssr_id],
                                                 local_address=Setting.get_value('local_address'),
                                                 local_port=int(local_port),
                                                 timeout=int(Setting.get_value('timeout')),
                                                 workers=int(Setting.get_value('workers')))
        else:
            ControlShadowsocksr.operate_on_unix(update_shadowsocksr.ssr_dict_list[ssr_id],
                                                local_address=Setting.get_value('local_address'),
                                                local_port=int(local_port),
                                                timeout=int(Setting.get_value('timeout')),
                                                workers=int(Setting.get_value('workers')),
                                                daemon="start",
                                                pid_file=Setting.get_value('shadowsocksr_pid_file_path'),
                                                log_file=Setting.get_value('shadowsocksr_log_file_path'))

    @staticmethod
    @is_id_valid(update_shadowsocksr.ssr_dict_list)
    def stop(ssr_id, local_port):
        ControlShadowsocksr.operate_on_unix(update_shadowsocksr.ssr_dict_list[ssr_id],
                                            local_address=Setting.get_value('local_address'),
                                            local_port=int(local_port),
                                            timeout=int(Setting.get_value('timeout')),
                                            workers=int(Setting.get_value('workers')),
                                            daemon="stop",
                                            pid_file=Setting.get_value('shadowsocksr_pid_file_path'),
                                            log_file=Setting.get_value('shadowsocksr_log_file_path'))

    @staticmethod
    def select_fast_node(local_port):
        ping_list = list()
        for ssr_dict in update_shadowsocksr.ssr_dict_list:
            if ssr_dict['ping'] == '∞':
                ping = 10000
            else:
                ping = float(ssr_dict['ping'])
            ping_list.append(ping)
        index = ping_list.index(min(ping_list))
        logger.info("Select fast node id - {0} Name - {1} Delay - {2}ms".
                    format(index, update_shadowsocksr.ssr_dict_list[index]['remarks'], ping_list[index]))
        HandleShadowsocksr.start(ssr_id=index, local_port=int(local_port))


class UpdateSystemProxy(object):
    """设置系统代理模式

    """

    def __init__(self):
        pass

    @staticmethod
    @is_ubuntu
    def open_global_proxy(local_port):
        cmd = "gsettings set org.gnome.system.proxy mode 'manual'"
        os.system(cmd)
        cmd = "gsettings set org.gnome.system.proxy.socks host {0}".format(Setting.get_value('local_address'))
        os.system(cmd)
        cmd = "gsettings set org.gnome.system.proxy.socks port {0}".format(local_port)
        os.system(cmd)
        logger.info("open global socks5 proxy - {0}:{1}".format(Setting.get_value('local_address'),
                                                                local_port))

    @staticmethod
    @is_ubuntu
    def open_pac_proxy(local_port, http_port=80):
        HandleHttpServer.handle_http_server("start", local_port, http_port)

        cmd = "gsettings set org.gnome.system.proxy autoconfig-url http://{0}:{1}/autoproxy.pac". \
            format(Setting.get_value('local_address'), http_port)
        os.system(cmd)
        logger.info('Open pac proxy - {0}:{1}'.format(Setting.get_value('local_address'), local_port))

    @staticmethod
    @is_ubuntu
    def close_proxy(local_port, http_port=80):
        cmd = "gsettings set org.gnome.system.proxy mode 'none'"
        os.system(cmd)
        HandleHttpServer.handle_http_server("stop", local_port, http_port)
        logger.info("Close system proxy")


class GenerateClashConfig(object):
    """生成clash配置文件

    属性:
        emojis: 节点标志字典
    """

    emojis = {
        "China": "🇨🇳",
        "Hongkong": "🇭🇰",
        "Taiwan": "🇹🇼",
        "Japan": "🇯🇵",
        "Singapore": "🇸🇬",
        "America": "🇺🇸",
        "Korea": "🇰🇷",
        "Others": "🏳‍🌈"
    }

    def __init__(self):
        pass

    @staticmethod
    def get_clash_example_config():
        url = "https://tyrantlucifer.com/ssr/clashExample.yaml"
        result = requests.get(url)
        result.encoding = 'utf-8'
        with open(init_config.clash_config_file, 'w', encoding='utf-8') as file:
            file.write(result.text)
        with open(init_config.clash_config_file, 'r', encoding='utf-8') as file:
            yaml_dict = yaml.safe_load(file)
        return yaml_dict

    @staticmethod
    def convert_country(ssr_dict_list):
        remarks = ssr_dict_list['remarks']
        if re.search(r'.*日.*|.*日本.*', remarks):
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['Japan'] + ' ' + remarks
            ssr_dict_list['country'] = "Japan"
        elif re.search(r'.*港.*|.*香港.*', remarks):
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['Hongkong'] + ' ' + remarks
            ssr_dict_list['country'] = "Hongkong"
        elif re.search(r'.*湾.*|.*台湾.*', remarks):
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['Taiwan'] + ' ' + remarks
            ssr_dict_list['country'] = "Taiwan"
        elif re.search(r'.*新.*|.*新加坡.*', remarks):
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['Singapore'] + ' ' + remarks
            ssr_dict_list['country'] = "Singapore"
        elif re.search(r'.*美.*|.*美国.*', remarks):
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['America'] + ' ' + remarks
            ssr_dict_list['country'] = "America"
        elif re.search(r'.*韩.*|.*韩国.*', remarks):
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['Korea'] + ' ' + remarks
            ssr_dict_list['country'] = "Korea"
        else:
            ssr_dict_list['remarks'] = GenerateClashConfig.emojis['Others'] + ' ' + remarks
            ssr_dict_list['country'] = "Others"

    @staticmethod
    def generate_clash_proxy_dict(ssr_dict_list):
        clash_proxy_dict = dict()
        clash_proxy_dict['server'] = ssr_dict_list['server']
        clash_proxy_dict['name'] = ssr_dict_list['remarks']
        clash_proxy_dict['port'] = ssr_dict_list['server_port']
        clash_proxy_dict['type'] = "ssr"
        clash_proxy_dict['cipher'] = ssr_dict_list['method']
        clash_proxy_dict['password'] = ssr_dict_list['password']
        clash_proxy_dict['protocol'] = ssr_dict_list['protocol']
        clash_proxy_dict['obfs'] = ssr_dict_list['obfs']
        clash_proxy_dict['protocol-param'] = ssr_dict_list['protocol_param']
        clash_proxy_dict['obfs-param'] = ssr_dict_list['obfs_param']
        return clash_proxy_dict

    @staticmethod
    def generate_clash_config():
        yaml_dict = GenerateClashConfig.get_clash_example_config()
        proxy_list = list()
        hk_proxy_dict = {
            'name': 'HK',
            'type': 'select',
            'proxies': []
        }
        sg_proxy_dict = {
            'name': 'SG',
            'type': 'select',
            'proxies': []
        }
        tw_proxy_dict = {
            'name': 'TW',
            'type': 'select',
            'proxies': []
        }
        jp_proxy_dict = {
            'name': 'JP',
            'type': 'select',
            'proxies': []
        }
        us_proxy_dict = {
            'name': 'US',
            'type': 'select',
            'proxies': []
        }
        ko_proxy_dict = {
            'name': 'KO',
            'type': 'select',
            'proxies': []
        }
        other_proxy_dict = {
            'name': 'OTHER',
            'type': 'select',
            'proxies': []
        }
        for ssr_dict in update_shadowsocksr.ssr_dict_list:
            GenerateClashConfig.convert_country(ssr_dict)
            if ssr_dict['country'] == 'Japan':
                jp_proxy_dict['proxies'].append(ssr_dict['remarks'])
            elif ssr_dict['country'] == 'Hongkong':
                hk_proxy_dict['proxies'].append(ssr_dict['remarks'])
            elif ssr_dict['country'] == 'Taiwan':
                tw_proxy_dict['proxies'].append(ssr_dict['remarks'])
            elif ssr_dict['country'] == 'Singapore':
                sg_proxy_dict['proxies'].append(ssr_dict['remarks'])
            elif ssr_dict['country'] == 'America':
                us_proxy_dict['proxies'].append(ssr_dict['remarks'])
            elif ssr_dict['country'] == 'Korea':
                ko_proxy_dict['proxies'].append(ssr_dict['remarks'])
            else:
                other_proxy_dict['proxies'].append(ssr_dict['remarks'])
            proxy_list.append(GenerateClashConfig.generate_clash_proxy_dict(ssr_dict))
        yaml_dict['proxies'] = proxy_list
        yaml_dict['proxy-groups'].append(hk_proxy_dict)
        yaml_dict['proxy-groups'].append(sg_proxy_dict)
        yaml_dict['proxy-groups'].append(tw_proxy_dict)
        yaml_dict['proxy-groups'].append(us_proxy_dict)
        yaml_dict['proxy-groups'].append(ko_proxy_dict)
        yaml_dict['proxy-groups'].append(jp_proxy_dict)
        yaml_dict['proxy-groups'].append(other_proxy_dict)
        with open(init_config.clash_config_file, 'w', encoding='utf-8') as file:
            yaml.dump(yaml_dict, file, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        logger.info("Generate clash config yaml successfully.")
        logger.info("You can find it on {0}".format(init_config.clash_config_file))


class HandleHttpServer(object):
    """控制本地http server

    """

    def __init__(self):
        pass

    @staticmethod
    def start(local_port, http_port=80):
        GeneratePac.generate_pac(Setting.get_value("local_address"), local_port)
        if init_config.platform == 'win32':
            http_local_server.start_on_windows(http_port=http_port)
        else:
            http_local_server.start(init_config.http_log_file,
                                    http_port=http_port)

    @staticmethod
    def stop():
        GeneratePac.remove_pac()
        http_local_server.stop()

    @staticmethod
    def handle_http_server(action, local_port, http_port=80):
        if action == "start":
            HandleHttpServer.start(local_port, http_port=http_port)
        elif action == "stop":
            if init_config.platform == "win32":
                logger.error("Only support unix platform")
            else:
                HandleHttpServer.stop()
        elif action == "status":
            if init_config.platform == "win32":
                logger.error("Only support unix platform")
            else:
                logger.info("HTTP Server status:{0}".format(http_local_server.is_running()))
        else:
            logger.error("--http not support this option: {0}".format(action))
