# shadowsocks-cli

![GitHub release (latest by date)](https://img.shields.io/github/v/release/tyrantlucifer/ssr-command-client)

English | [中文](README_CH.md) 

The command client of shadowsocksr based by python

## Features

- Support `Linux` + `Windows` + `Mac` all platforms
- Support parse shadowsocksr url
- Support parse multi shadowsocksr subscribe urls
- Support assign the port of local proxy
- Support test shadowsockr node delay
- Support test shadowsocksr node is or not blocked by tcp
- Support test shadowsocksr node download and upload speed
- Support test node Netflix unlocking situation
- Support generate json and qrcode for shadowsocksr node
- Support generate clash config file for your shadowsocksr subscribe
- Support open http pac proxy
- Not Support ipv6 shadowsocksr node
- Developed by pure python

## Install

- install using source code
```shell
git clone https://github.com/TyrantLucifer/ssr-command-client.git
cd ssr-command-client
python(python3) setup.py install
```

- install using pip tool
```shell
pip(pip3) install shadowsocksr-cli
```

## Usage
```angular2html
usage: shadowsocksr-cli [-h] [-l] [-p local_port] [-s ssr_id]       
                        [-S [ssr_id]] [-u] [-v] [--generate-clash]  
                        [--display-json ssr_id]
                        [--test-speed ssr_id]                       
                        [--test-netflix ssr_id] [--test-netflix-all]
                        [--fast-node]                               
                        [--setting-url ssr_subscribe_url]           
                        [--setting-address ssr_local_address]       
                        [--list-url] [--add-url ssr_subscribe_url]  
                        [--remove-url ssr_subscribe_url]
                        [--list-address] [--parse-url ssr_url]        
                        [--add-ssr ssr_url]
                        [--test-again ssr_node_id]
                        [--print-qrcode ssr_node_id]
                        [--http action[start stop status]]
                        [--http-port http server port]
                        [--setting-global-proxy]
                        [--setting-pac-proxy] [--close-system-proxy]  

The shadowsocksr command client based Python.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            show ssr list
  -p local_port, --port local_port
                        assign local proxy port,use with -s
  -s ssr_id, --start ssr_id
                        start ssr proxy
  -S [ssr_id], --stop [ssr_id]
                        stop ssr proxy
  -u, --update          update ssr list
  -v, --version         display version
  --generate-clash      generate clash config yaml
  --display-json ssr_id
                        display ssr json info
  --test-speed ssr_id   test ssr nodes download and upload speed      
  --test-netflix ssr_id
                        test ssr nodes if or not watch netflix        
  --test-netflix-all    test all ssr nodes if or not watch netflix    
  --fast-node           find most fast by delay and start ssr proxy   
  --setting-url ssr_subscribe_url
                        setting ssr subscribe url
  --setting-address ssr_local_address
                        setting ssr local address
  --list-url            list ssr subscribe url
  --add-url ssr_subscribe_url
                        add ssr subscribe url
  --remove-url ssr_subscribe_url
                        remove ssr subscribe url
  --list-address        list ssr local address
  --parse-url ssr_url   pares ssr url
  --add-ssr ssr_url     add ssr node
  --test-again ssr_node_id
                        test ssr node again
  --print-qrcode ssr_node_id
                        print ssr node qrcode
  --http action[start stop status]
                        Manager local http server
  --http-port http server port
                        assign local http server port
  --setting-global-proxy
                        setting system global proxy,only support on   
                        Ubuntu Desktop
  --setting-pac-proxy   setting system pac proxy,only support on      
                        Ubuntu Desktop
  --close-system-proxy  close system proxy,only support on
                        Ubuntu Desktop
```

## Simple Examples

```angular2html
Supposed your shadowsocksr nodes list as below：
+----+----------------------------+-----------+---------+----------------+------+-------------+
| id |            name            | delay(ms) | connect |     server     | port |    method   |
+----+----------------------------+-----------+---------+----------------+------+-------------+
| 0  |    SSRTOOL_Node:新加坡-    |     100     |    √    | 172.104.161.54 | 8099 | aes-256-cfb |
| 1  | SSRTOOL_Node:美国-密苏里州  |     200     |    √    |  69.30.201.82  | 8099 | aes-256-cfb |
+----+----------------------------+-----------+---------+----------------+------+-------------+
```
- open the us proxy ` shadowsocksr-cli -s 1`
- print the list of all nodes ` shadowsocksr-cli -l`
- update subscribe list ` shadowsocksr-cli -u`
- reset shadowsocksr subcribe url ` shadowsocksr-cli --setting-url https://tyrantlucifer.com/ssr/ssr.txt`
- print the current subcribe urls that you had been setting ` shadowsocksr-cli --list-url`
- print the listen address ` shadowsocksr-cli --list-address`

## API

- parse shadowsocksr node information by shadowsocksr url, shadowsocksr url must be looked like 'ssr://xxxxx'

```python
import json
from shadowsocksr_cli.parse_utils import *

ssr_url = "ssr://NjkuMzAuMjAxLjgyOjgwOTk6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOlpVbFhNRVJ1YXpZNU5EVTBaVFp1VTNkMWMzQjJPVVJ0VXpJd01YUlJNRVEvP3JlbWFya3M9VTFOU1ZFOVBURjlPYjJSbE91ZS1qdVdidlMzbHI0Ym9pNF9waDR6bHQ1NCZncm91cD1WMWRYTGxOVFVsUlBUMHd1UTA5Tg"
ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
print(json.dumps(ssr_dict,
                 ensure_ascii=False,
                 indent=4))
```

- get the connect information of a shadowsocksr node by shadowsocksr url, shadowsocksr url must be looked like 'ssr://xxxxx'
```python
from shadowsocksr_cli.parse_utils import *
from shadowsocksr_cli.network_test_utils import *

ssr_url = "ssr://NjkuMzAuMjAxLjgyOjgwOTk6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOlpVbFhNRVJ1YXpZNU5EVTBaVFp1VTNkMWMzQjJPVVJ0VXpJd01YUlJNRVEvP3JlbWFya3M9VTFOU1ZFOVBURjlPYjJSbE91ZS1qdVdidlMzbHI0Ym9pNF9waDR6bHQ1NCZncm91cD1WMWRYTGxOVFVsUlBUMHd1UTA5Tg"
ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
ssr_dict = ShadowsocksrTest.test_shadowsocksr_connect(ssr_dict)
print(ssr_dict['connect'],
      ssr_dict['ping'])
```

- test shadowsocksr node download and upload information by shadowsocksr url, shadowsocksr url must be looked like 'ssr://xxxxx'
```python
from shadowsocksr_cli.parse_utils import *
from shadowsocksr_cli.network_test_utils import *

ssr_url = "ssr://NjkuMzAuMjAxLjgyOjgwOTk6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOlpVbFhNRVJ1YXpZNU5EVTBaVFp1VTNkMWMzQjJPVVJ0VXpJd01YUlJNRVEvP3JlbWFya3M9VTFOU1ZFOVBURjlPYjJSbE91ZS1qdVdidlMzbHI0Ym9pNF9waDR6bHQ1NCZncm91cD1WMWRYTGxOVFVsUlBUMHd1UTA5Tg"
ssr_dict = ParseShadowsocksr.parse_shadowsocksr(ssr_url)
ssr_dict = ShadowsocksrTest.test_shadowsocksr_connect(ssr_dict)
ShadowsocksrTest.test_shadowsocksr_speed(ssr_dict)
```

## How to use proxy in linux shell

- setting proxy for linux shell `export ALL_PROXY=socks5://127.0.0.1:1080`
- you can use this command to test is or not you setting proxy successfully `curl http://ip-api.com/json/?lang=zh-CN`
- unset proxy for linux shell `unset ALL_PROXY`
- add the following content in you `~/.bashrc` is a best practise
```shell
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1080"
alias unsetproxy="unset ALL_PROXY"
alias ip="curl http://ip-api.com/json/?lang=zh-CN"
```
- if you prefer socks5 to http proxy, you can use this command `shadowsocksr-cli -p 1080 --http-proxy start --http-proxy-port 7890`
- then you can add the following content in you `~/.bashrc`
```shell
alias sethttpsproxy="export HTTPS_PROXY=http://127.0.0.1:7890"
alias unsethttpsproxy="unset HTTPS_PROXY"
```

## Support open source:heart:, Buy the author a Starbucks

> If you are willing to donate, please write your Github account in the donation note. Thank you  

| wechat                                                                                                     | alipay                                                                                                       |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| <a href='#支持开源'><img src="https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/wechat-pay.png" height="150" width="150" /></a> | <a href='#支持开源'><img src="https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/alipay.jpg" height="150" width="150" /></a> |

| ID | Sponsors                                | RMB  | Time   |
| ---- | ------------------------------------- | ---- | ---------- |
| 1    | [lfp1024](https://github.com/lfp1024) | 20   | 2021-09-12 |
| 2    | [mmin18](https://github.com/mmin18) | 30   | 2021-12-31 |
| 3    | unknown | 20   | 2022-04-15 |
| 4    | unknown | 30   | 2022-04-28 |
| 5    | [jmydurant](https://github.com/jmydurant) | 50   | 2022-04-28 |
| 6    | unknown | 5.21   | 2023-01-08 |
| 7    | unknown | 20   | 2023-04-20 |

## Thanks

I would like to thank Jetbrains for supporting the legitimate tool for developing this project. If there is a commercial need, I recommend purchasing the legitimate tool  [Jetbrains](https://www.jetbrains.com/?from=ssr-command-client)

|Jetbrains|
|---------|
|<a href='#致谢'><img src="https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/jetbrains-variant-2.png" height="300" width="300" /></a> |

## Stargazers over time

[![Stargazers over time](https://starchart.cc/TyrantLucifer/ssr-command-client.svg)](https://starchart.cc/TyrantLucifer/ssr-command-client)
