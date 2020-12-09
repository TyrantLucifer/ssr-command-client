from utils.InitUtils import *
from utils.HandleSSRUtils import *
from utils.PrintUtils import *
from utils.SSRTestUtils import *
from utils.SettingUtils import *
from utils.ParseUtils import *

i = InitConfigDir()
settings = Setting(i.configFilePath)
u = UpdateSubscribeUrl(i.ssrListJsonFile, settings.valueDict['subscribe_url'])
h = ControlSSR()
ssrTable = DrawInfoListTable()

class Hanlder(object):

    def __init__(self):
        pass

    def start(self, id, port=1080):
        if i.platform == 'win32':
            h.startOnWindows(u.ssrInfoList[id], settings.valueDict['local_address'],
                             port,
                             settings.valueDict['timeout'],
                             settings.valueDict['workers'])

    def stop(self):
        pass

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



class Display(object):

    def __init__(self):
        pass

    def displaySSRList(self):
        for ssrInfo in u.ssrInfoList:
            ssrTable.append(
                id=ssrInfo['id'],
                name=ssrInfo['remarks'],
                ping=ssrInfo['ping'],
                connect=ssrInfo['connect'],
                server=ssrInfo['server'],
                port=ssrInfo['server_port'],
                method=ssrInfo['method']
            )
        ssrTable.print()

    def displaySSRSpeedList(self):
        pass

    def displaySuscribeUrl(self):
        for url in u.urlList:
            color.print(url, 'blue')


    def displayLocalAddress(self):
        color.print(settings.valueDict['local_address'],
                    'blue')

    def displaySSRJson(self, id):
        i.createJsonFile(u.ssrInfoList[id])
        color.print(json.dumps(u.ssrInfoList[id], ensure_ascii=False, indent=4),
                    'yellow')

    def parseSSRUrl(self, ssrUrl):
        ssrInfo = ParseShadowsocksR.parseShadowsocksR(ssrUrl)
        ssrInfo = s.testSSRConnect(ssrInfo)
        color.print(json.dumps(ssrInfo, ensure_ascii=False, indent=4),
                    'yellow')
