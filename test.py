'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午6:24
'''

from utils.InitUtils import *
from utils.ParseUtils import *
from utils.SettingUtils import *
from utils.SSRTestUtils import *
from speedtest import speedtest

i = InitConfigDir()
g = GetSubscribeUrl()
s = SSRSpeedTest()
settings = Setting(i.configFilePath)
subscribeUrlList = settings.valueDict['SUBSCRIBE_URL'].split(',')
resultList = g.requestUrlList(subscribeUrlList)
ssrList = g.getNodeInfoList()

# if __name__ == "__main__":
#     threadList = s.threadPool(s.testSSRConnect, ssrList)
#     for thread in threadList:
#         print(thread.get())

