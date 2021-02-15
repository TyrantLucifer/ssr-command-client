from utils.InitUtils import *
from utils.SettingUtils import *
from utils.ParseUtils import *

i = InitConfigDir()
settings = Setting(i.configFilePath)
u = UpdateSubscribeUrl(i.ssrListJsonFile, settings.valueDict['subscribe_url'])
h = ControlSSR()
ssrTable = DrawInfoListTable()
ssrSpeedTable = DrawSpeedTable()


def is_id_valid(func):
    def judge(*args, **kwargs):
        if kwargs['ssr_id'] < 0 or kwargs['ssr_id'] >= len(u.ssrInfoList):
            logger.error('ssr id error')
            sys.exit(1)
        else:
            ssrLogger.addHandler(streamHandler)
            func(*args, **kwargs)
            ssrLogger.removeFilter(streamHandler)

    return judge


def is_ubuntu(func):
    def judge(*args, **kwargs):
        if i.system != 'Ubuntu':
            logger.info("Current OS - {0} {1} only support Ubuntu".format(i.system, func.__name__))
            sys.exit(1)
        else:
            func(*args, **kwargs)

    return judge


class Handler(object):

    def __init__(self):
        pass

    @is_id_valid
    def start(self, ssr_id, port=1080):
        if i.platform == 'win32':
            h.startOnWindows(u.ssrInfoList[ssr_id], settings.local_address,
                             port,
                             settings.timeout,
                             settings.workers)
        else:
            h.startOnUnix(u.ssrInfoList[ssr_id], settings.local_address,
                          port,
                          settings.timeout,
                          settings.workers,
                          i.pidFilePath,
                          i.logFilePath)

    @is_id_valid
    def stop(self, ssr_id, port=1080):
        h.stopOnUnix(u.ssrInfoList[ssr_id], settings.local_address,
                     port,
                     settings.timeout,
                     settings.workers,
                     i.pidFilePath,
                     i.logFilePath)
        os.remove(i.pidFilePath)

    def startFastNode(self):
        pingList = list()
        for ssrInfo in u.ssrInfoList:
            if ssrInfo['ping'] == '∞':
                ping = 10000
            else:
                ping = float(ssrInfo['ping'])
            pingList.append(ping)
        index = pingList.index(min(pingList))
        logger.info("select fast node id - {0} name - {1} delay - {2}ms".
                    format(index, u.ssrInfoList[index]['remarks'], pingList[index]))
        self.start(ssr_id=index)

    @is_ubuntu
    def openGlobalProxy(self):
        cmd = "gsettings set org.gnome.system.proxy mode 'manual'"
        os.system(cmd)
        cmd = "gsettings set org.gnome.system.proxy.socks host {0}".format(settings.local_address)
        os.system(cmd)
        cmd = "gsettings set org.gnome.system.proxy.socks port {0}".format(1080)
        os.system(cmd)
        logger.info("open global socks5 proxy - {0}:{1}".format(settings.local_address, 1080))

    @is_ubuntu
    def openPacProxy(self):
        logger.info("start to create pac file, it will take a lot of time")
        result = requests.get('https://tyrantlucifer.com/ssr/autoproxy.pac')
        result.encoding = 'utf-8'
        with open(i.pacFilePath, 'w', encoding='utf-8') as file:
            file.write(result.text)
        logger.info('generate pac file successfully')
        cmd = "gsettings set org.gnome.system.proxy autoconfig-url file://{0}".format(i.pacFilePath)
        os.system(cmd)
        logger.info('open pac proxy - {0}:{1}'.format(settings.local_address, 1080))

    @is_ubuntu
    def closeProxy(self):
        cmd = "gsettings set org.gnome.system.proxy mode 'none'"
        os.system(cmd)
        logger.info("close system proxy")


class Update(object):

    def __init__(self):
        pass

    def updateSubscribe(self):
        ssrInfoList = u.update(i.ssrListJsonFile,
                               settings.valueDict['subscribe_url'].split('|'))
        ssrInfoList = s.startConnectTest(ssrInfoList)
        u.updateCacheJson(i.ssrListJsonFile, ssrInfoList)
        u.ssrInfoList = ssrInfoList

    def updateSubcribeUrl(self, url):
        settings.setValue('subscribe_url', url)
        logger.info('change subscribe url to: {0}'.format(url))

    def updateLocalAddress(self, address):
        settings.setValue('local_address', address)
        logger.info('change subscribe url to: {0}'.format(address))

    def testSSRSpeed(self):
        ssrInfoList = s.startSpeedTest(u.ssrInfoList)
        for ssrInfo in ssrInfoList:
            if ssrInfo['connect']:
                download = color.green(str(ssrInfo['download']))
                upload = color.green(str(ssrInfo['upload']))
            else:
                download = color.red(ssrInfo['download'])
                upload = color.red(ssrInfo['upload'])

            ssrSpeedTable.append(
                id=ssrInfo['id'],
                name=ssrInfo['remarks'],
                download=download,
                upload=upload,
                server=ssrInfo['server'],
                port=ssrInfo['server_port'],
                method=ssrInfo['method']
            )
        ssrSpeedTable.print()

    def addSSRNode(self, ssrUrl):
        ssrInfo = ParseShadowsocksR.parseShadowsocksR(ssrUrl)
        ssrInfo = s.testSSRConnect(ssrInfo)
        ssrInfo['id'] = len(u.ssrInfoList)
        u.ssrInfoList.append(ssrInfo)
        u.updateCacheJson(i.ssrListJsonFile, u.ssrInfoList)

    def addSSRSubcribeUrl(self, subscribeUrl):
        u.urlList.append(subscribeUrl)
        settings.setValue('subscribe_url',
                          '|'.join(u.urlList))
        logger.info('add subscribe_url url: {0}'.format(subscribeUrl))

    def removeSSRSubcribeUrl(self, subcribeUrl):
        if subcribeUrl in u.urlList:
            u.urlList.remove(subcribeUrl)
            settings.setValue('subscribe_url',
                              '|'.join(u.urlList))
            logger.info("remove subcribeUrl - {0}".
                        format(subcribeUrl))
        else:
            logger.error("subscribeUrl - {0} is not existed".
                         format(subcribeUrl))

    @is_id_valid
    def testSSRNodeConnect(self, ssr_id):
        u.ssrInfoList[ssr_id] = s.testSSRConnect(u.ssrInfoList[ssr_id])
        logger.info('test node successfully, connect: {0} delay: {1}'.
                    format(u.ssrInfoList[ssr_id]['connect'], u.ssrInfoList[ssr_id]['ping']))
        u.updateCacheJson(i.ssrListJsonFile, u.ssrInfoList)


class Display(object):

    def __init__(self):
        pass

    def displaySSRList(self):
        for ssrInfo in u.ssrInfoList:
            if ssrInfo['connect']:
                delay = color.green(ssrInfo['ping'])
                connect = color.green('√')
            else:
                delay = color.red(ssrInfo['ping'])
                connect = color.red('×')

            ssrTable.append(
                id=ssrInfo['id'],
                name=ssrInfo['remarks'],
                delay=delay,
                connect=connect,
                server=ssrInfo['server'],
                port=ssrInfo['server_port'],
                method=ssrInfo['method']
            )
        ssrTable.print()

    def displaySuscribeUrl(self):
        for url in u.urlList:
            color.print(url, 'blue')

    def displayLocalAddress(self):
        color.print(settings.local_address, 'blue')

    @is_id_valid
    def displaySSRJson(self, ssr_id):
        i.createJsonFile(u.ssrInfoList[ssr_id])
        color.print(json.dumps(u.ssrInfoList[ssr_id], ensure_ascii=False, indent=4),
                    'yellow')

    def parseSSRUrl(self, ssrUrl):
        ssrInfo = ParseShadowsocksR.parseShadowsocksR(ssrUrl)
        ssrInfo = s.testSSRConnect(ssrInfo)
        color.print(json.dumps(ssrInfo, ensure_ascii=False, indent=4),
                    'yellow')

    def displayVersion(self):
        logger.info("start get version from cloud, it will take a lot of time")
        result = requests.get('https://tyrantlucifer.com/ssr/version.json')
        result.encoding = 'utf-8'
        version = result.json()['version']
        tips_message = result.json()['tips_message']
        if version == i.version:
            logger.info("Current version {0} is newest. Please enjoy.".format(version))
        else:
            logger.info("Current version: {0}".format(i.version))
            logger.info("Newest version: {0}, "
                        "you can download on https://github.com/TyrantLucifer/ssr-command-client/releases/tag/v{1}".
                        format(version, version))
        logger.info(tips_message)

    @calculate
    def upgrade(self):
        logger.info("start get version from cloud, it will take a lot of time")
        result = requests.get('https://tyrantlucifer.com/ssr/version.json')
        result.encoding = 'utf-8'
        version = result.json()['version']
        if version == i.version:
            logger.info("Current version {0} is newest. Please enjoy.".format(version))
        else:
            logger.info("Current version: {0}".format(i.version))
            logger.info("Newest version: {0}".format(version))
            logger.info("Start update ssr-command-client...")
            if i.platform == 'win32':
                file_name = 'ssr-command-client_windows_amd64.exe'
            else:
                file_name = 'ssr-command-client_linux_amd64'
            r = requests.get('https://tyrantlucifer.com/ssr/releases/{0}'.format(file_name))
            with open(os.path.join(i.homeDir, file_name), 'wb') as file:
                file.write(r.content)
            logger.info("Update success. Please enjoy it.")
            logger.info("You can find binary file in {0}".format(i.homeDir))

    @is_id_valid
    def printQrCode(self, ssr_id):
        PrintQrcode.print_qrcode(u.ssrInfoList[ssr_id]['ssr_url'])


class GenerateConfig(object):

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

    def __readClashExampleConfig(self):
        url = "https://tyrantlucifer.com/ssr/clashExample.yaml"
        result = requests.get(url)
        result.encoding = 'utf-8'
        with open(i.clashConfigFilePath, 'w', encoding='utf-8') as file:
            file.write(result.text)
        with open(i.clashConfigFilePath, 'r', encoding='utf-8') as file:
            yaml_dict = yaml.safe_load(file)
        return yaml_dict

    def __convertCountry(self, ssr_info_dict):
        remarks = ssr_info_dict['remarks']
        if re.search(r'.*日.*|.*日本.*', remarks):
            ssr_info_dict['remarks'] = self.emojis['Japan'] + ' ' + remarks
            ssr_info_dict['country'] = "Japan"
        elif re.search(r'.*港.*|.*香港.*', remarks):
            ssr_info_dict['remarks'] = self.emojis['Hongkong'] + ' ' + remarks
            ssr_info_dict['country'] = "Hongkong"
        elif re.search(r'.*湾.*|.*台湾.*', remarks):
            ssr_info_dict['remarks'] = self.emojis['Taiwan'] + ' ' + remarks
            ssr_info_dict['country'] = "Taiwan"
        elif re.search(r'.*新.*|.*新加坡.*', remarks):
            ssr_info_dict['remarks'] = self.emojis['Singapore'] + ' ' + remarks
            ssr_info_dict['country'] = "Singapore"
        elif re.search(r'.*美.*|.*美国.*', remarks):
            ssr_info_dict['remarks'] = self.emojis['America'] + ' ' + remarks
            ssr_info_dict['country'] = "America"
        elif re.search(r'.*韩.*|.*韩国.*', remarks):
            ssr_info_dict['remarks'] = self.emojis['Korea'] + ' ' + remarks
            ssr_info_dict['country'] = "Korea"
        else:
            ssr_info_dict['remarks'] = self.emojis['Others'] + ' ' + remarks
            ssr_info_dict['country'] = "Others"

    def generateClashProxyDict(self, ssr_info_dict):
        clash_proxy_dict = dict()
        clash_proxy_dict['server'] = ssr_info_dict['server']
        clash_proxy_dict['name'] = ssr_info_dict['remarks']
        clash_proxy_dict['port'] = ssr_info_dict['server_port']
        clash_proxy_dict['type'] = "ssr"
        clash_proxy_dict['cipher'] = ssr_info_dict['method']
        clash_proxy_dict['password'] = ssr_info_dict['password']
        clash_proxy_dict['protocol'] = ssr_info_dict['protocol']
        clash_proxy_dict['obfs'] = ssr_info_dict['obfs']
        clash_proxy_dict['protocol-param'] = ssr_info_dict['protocol_param']
        clash_proxy_dict['obfs-param'] = ssr_info_dict['obfs_param']
        return clash_proxy_dict

    def generateClashConfig(self):
        yaml_dict = self.__readClashExampleConfig()
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
        for ssr_info_dict in u.ssrInfoList:
            self.__convertCountry(ssr_info_dict)
            if ssr_info_dict['country'] == 'Japan':
                jp_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            elif ssr_info_dict['country'] == 'Hongkong':
                hk_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            elif ssr_info_dict['country'] == 'Taiwan':
                tw_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            elif ssr_info_dict['country'] == 'Singapore':
                sg_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            elif ssr_info_dict['country'] == 'America':
                us_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            elif ssr_info_dict['country'] == 'Korea':
                ko_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            else:
                other_proxy_dict['proxies'].append(ssr_info_dict['remarks'])
            proxy_list.append(self.generateClashProxyDict(ssr_info_dict))
        yaml_dict['proxies'] = proxy_list
        yaml_dict['proxy-groups'].append(hk_proxy_dict)
        yaml_dict['proxy-groups'].append(sg_proxy_dict)
        yaml_dict['proxy-groups'].append(tw_proxy_dict)
        yaml_dict['proxy-groups'].append(us_proxy_dict)
        yaml_dict['proxy-groups'].append(ko_proxy_dict)
        yaml_dict['proxy-groups'].append(jp_proxy_dict)
        yaml_dict['proxy-groups'].append(other_proxy_dict)
        with open(i.clashConfigFilePath, 'w', encoding='utf-8') as file:
            yaml.dump(yaml_dict, file, default_flow_style=False,encoding='utf-8',allow_unicode=True)
        logger.info("Generate clash config yaml successfully. You can find it on {0}".format(i.clashConfigFilePath))

