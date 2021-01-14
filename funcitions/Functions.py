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
                download = color.red(str(ssrInfo['download']))
                upload = color.red(str(ssrInfo['upload']))

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
        settings.setValue('subscribe_url',
                          settings.subscribe_url + '|' + subscribeUrl)
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
