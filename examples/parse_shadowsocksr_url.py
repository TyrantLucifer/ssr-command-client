"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: parse_shadowsocksr_url.py
@time: 2021/2/20 11:27
@desc: 使用shadowsocksr-cli api解析shadowsocksr链接
"""

import json
from shadowsocksr_cli.parse_utils import *


def main():
    ssr_url = "ssr://NjkuMzAuMjAxLjgyOjgwOTk6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOlpVbFhNRVJ1YXpZNU5EVTBaVFp1VTNkMWMzQjJPVVJ0VXpJd01YUlJNRVEvP3JlbWFya3M9VTFOU1ZFOVBURjlPYjJSbE91ZS1qdVdidlMzbHI0Ym9pNF9waDR6bHQ1NCZncm91cD1WMWRYTGxOVFVsUlBUMHd1UTA5Tg"
    ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
    print(json.dumps(ssr_dict,
                     ensure_ascii=False,
                     indent=4))


if __name__ == "__main__":
    main()
