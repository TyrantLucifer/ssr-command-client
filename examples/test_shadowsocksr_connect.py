"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: test_shadowsocksr_connect.py
@time: 2021/2/20 11:32
@desc: 使用shadowsocksr-cli 测试shadowsocksr节点连接状态
"""

from shadowsocksr_cli.parse_utils import *
from shadowsocksr_cli.network_test_utils import *


def main():
    ssr_url = "ssr://NjkuMzAuMjAxLjgyOjgwOTk6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOlpVbFhNRVJ1YXpZNU5EVTBaVFp1VTNkMWMzQjJPVVJ0VXpJd01YUlJNRVEvP3JlbWFya3M9VTFOU1ZFOVBURjlPYjJSbE91ZS1qdVdidlMzbHI0Ym9pNF9waDR6bHQ1NCZncm91cD1WMWRYTGxOVFVsUlBUMHd1UTA5Tg"
    ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
    ssr_dict = ShadowsocksrTest.test_shadowsocksr_connect(ssr_dict)
    print(ssr_dict['connect'],
          ssr_dict['ping'])


if __name__ == "__main__":
    main()
