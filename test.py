'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/6 下午6:24
'''

from multiprocessing import Pool
from utils.InitUtils import *
from utils.ParseUtils import GetSubscribeUrl
from utils.SettingUtils import Setting
from utils.SsrTestUtils import SsrSpeedTest

i = InitConfigDir()
g = GetSubscribeUrl()
settings = Setting(i.configFilePath)
s = SsrSpeedTest()

subscribeUrlList = settings.valueDict['SUBSCRIBE_URL'].split(',')
resultList = g.requestUrlList(subscribeUrlList)
ssrList = g.getNodeInfoList()
pool = Pool(len(ssrList))
thread = list()
for ssr in ssrList:
    t = pool.apply_async(s.testSsrNodes, (ssr,))
    thread.append(t)

pool.close()
pool.join()

for t in thread:
    print(t.get()['ping'])
