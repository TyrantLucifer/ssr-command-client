'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午6:24
'''

from utils.InitUtils import *
from utils.PrintUtils import *
from utils.ParseUtils import *
from utils.SettingUtils import *
from utils.SSRTestUtils import *
from utils.HandleSSRUtils import *

i = InitConfigDir()
g = UpdateSubscribeUrl()
s = SSRSpeedTest()
h = ControlSSR()
ssrTable = DrawInfoListTable()

settings = Setting(i.configFilePath)
subscribeUrlList = settings.valueDict['subscribe_url'].split(',')

ssrList = g.update(i.ssrListJsonFile, subscribeUrlList)
ssrList = s.startConnectTest(ssrList)
g.updateCacheJson(i.ssrListJsonFile, ssrList)