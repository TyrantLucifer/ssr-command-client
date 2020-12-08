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
ssrList = g.getNodeInfoList(i.ssrListJsonFile, subscribeUrlList)

# h.startOnWindows(ssrList[20], '127.0.0.1', 1080, 300, 1, i.pidFialePath, i.logFilePath)

if __name__ == "__main__":
    h.startOnWindows(ssrList[20], '127.0.0.1', 1080, 300, 1, i.pidFilePath, i.logFilePath)
# s.testSSRSpeed(ssrList[20], '127.0.0.1', 60000, 300, 1)
    # threadList = s.speedThreadPool(s.testSSRSpeed, ssrList)
    # for thread in threadList:
    #     print(thread.get())
#     ssrList = g.update(i.ssrListJsonFile, subscribeUrlList)
#     threadList = s.threadPool(s.testSSRConnect, ssrList)
#     ssrList.clear()
#     for thread in threadList:
#         ssrList.append(thread.get())
#     g.updateCacheJson(i.ssrListJsonFile, ssrList)
#     for ssr in ssrList:
#         ssrTable.append(
#             id=ssr['id'],
#             name=ssr['remarks'],
#             ping=ssr['ping'],
#             port_status=ssr['port_status'],
#             server=ssr['server'],
#             port=ssr['server_port'],
#             method=ssr['method']
#         )
#     ssrTable.print()

