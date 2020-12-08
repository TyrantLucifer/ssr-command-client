'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午6:24
'''

from logger.Logging import *
from utils.InitUtils import *
from utils.ParseUtils import *
from utils.SettingUtils import *
from utils.SSRTestUtils import *
from utils.HandleSSRUtils import *

i = InitConfigDir()
g = GetSubscribeUrl()
s = SSRSpeedTest()
h = ControlSSR()
settings = Setting(i.configFilePath)
subscribeUrlList = settings.valueDict['subscribe_url'].split(',')
resultList = g.requestUrlList(subscribeUrlList)
ssrList = g.getNodeInfoList()

h.start(ssrList[20], '127.0.0.1', 1080, 300, 1)

# if __name__ == "__main__":
#     threadList = s.threadPool(s.testSSRConnect, ssrList)
#     for thread in threadList:
#         print(thread.get())

