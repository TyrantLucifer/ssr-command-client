# The command client of ShadowsocksR based Python3

在命令行下使用的一款ShadowsocksR客户端

## 特性

- 全新`2.0`版本，在`1.0`基础上进行使用面向对象重构，并预留接口
- 支持`Linux` + `Windows`双平台
- 支持ShadowsocksR链接解析
- 支持ShadowsocksR订阅链接解析(支持添加多个订阅地址)
- 支持制定本地端口启动代理
- 支持测试ShadowsocksR节点真连接延迟(多线程)
- 支持测试ShadowsocksR节点是否被tcp阻断(多线程)
- 支持ShadowsocksR节点测速(多线程)
- 支持打印ShadowsocksR节点Json和二维码
- 整合ShadowsocksR源码到项目中
- 暂时不支持`ipv6`ShadowsocksR节点，解析时会默认屏蔽

## 安装方式

- 源码安装
```shell
git clone https://github.com/TyrantLucifer/ssr-command-client.git
cd ssr-command-client
python(pip3) install -r requirement.txt
```

- 下载二进制文件
> [Linux - ssr-command-client](https://github.com/TyrantLucifer/ssr-command-client/releases/download/v2.0/ssr-command-client_linux_amd64)

> [Windows - ssr-command-client](https://github.com/TyrantLucifer/ssr-command-client/releases/download/v2.0/ssr-command-client_windows_amd64.exe)

## 使用方法
```angular2html
usage: ssr-commnd-client [-h] [-l] [-p local_port] [-s ssr_id] [-S ssr_id] [-u] [-v]
                         [--display-json ssr_id] [--test-speed] [--fast-node]
                         [--setting-url ssr_subscribe_url]
                         [--setting-address ssr_local_address] [--list-url]
                         [--add-url ssr_subscribe_url] [--remove-url ssr_subscribe_url]
                         [--list-address] [--parse-url ssr_url] [--add-ssr ssr_url]
                         [--test-again ssr_node_id] [--print-qrcode ssr_node_id]
                         [--setting-global-proxy] [--setting-pac-proxy]
                         [--close-system-proxy] 

ShadowsocksR 命令行客户端

optional arguments:
  -v, --version         版本信息
  -h, --help            帮助信息

通用参数:

-l --list "show ssr list" 打印当前节点列表

-p --port PORT 指定端口，通常与 -s --start 一起使用

-s SSR_NODE_ID 启动Shadowsocks代理，SSR_NODE_ID为节点ID，可从打印列表中获得；
               如果不指定 -p 参数，那么默认代理启动在本地1080端口

-S SSR_NODE_ID 停止Shadowsocks代理，SSR_NODE_ID为节点ID，可从打印列表中获得；
               只在Linux系统中生效

-u --update 更新SSR订阅列表

--fast-node 根据节点真连接延迟自动选择最优节点，并在本地启动代理

--setting-url SUBSCRIBE_URL 重置ssr订阅链接，SUBSCRIBE_URL为订阅链接地址
                            注：如果订阅链接中有&符号，请用""将链接括起来

--setting-address LOCAL_ADDRESS 重置本地代理监听地址，默认监听地址为127.0.0.1
                                一般在想要分享代理给局域网设备的时候使用

--add-url SUBSCRIBE_URL 增加ssr订阅链接，SUBSCRIBE_URL为订阅链接地址
                        注：如果订阅链接中有&符号，请用""将链接括起来

--remove-url SUBSCRIBE_URL 移除ssr订阅链接，SUBSCRIBE_URL为订阅链接地址
                           注：如果订阅链接中有&符号，请用""将链接括起来

--list-address 打印当前本地监听地址

--list-url 打印当前已有订阅链接

--parse-url SSR_URL 解析ssr链接，SSR_URL为ssr链接地址，例如：ssr://xxxxxxxxxxxxxxxx

--add-ssr SSR_URL 手动添加ssr节点到当前列表中，SSR_URL为ssr链接地址，例如：ssr://xxxxxxxxxxxxxxxx

--test-again SSR_NODE_ID 重新测试ssr节点连接状态，SSR_NODE_ID为节点ID，可从打印列表中获得

--test-speed 批量ssr节点测速

--print-qrcode SSR_NODE_ID 打印ssr节点二维码，SSR_NODE_ID为节点ID，可从打印列表中获得

--setting-global-proxy 设置全局代理为本地socks5代理，注：只支持Ubuntu Desktop

--setting-pac-proxy 设置pac代理，注：只支持Ubuntu Desktop

--close-system-proxy 关闭系统代理选项，注：只支持Ubuntu Desktop

```

## 简单示例

```angular2html
假设你的订阅链接节点列表为如下：
+----+----------------------------+-----------+---------+----------------+------+-------------+
| id |            name            | delay(ms) | connect |     server     | port |    method   |
+----+----------------------------+-----------+---------+----------------+------+-------------+
| 0  |    SSRTOOL_Node:新加坡-    |     100     |    √    | 172.104.161.54 | 8099 | aes-256-cfb |
| 1  | SSRTOOL_Node:美国-密苏里州  |     200     |    √    |  69.30.201.82  | 8099 | aes-256-cfb |
+----+----------------------------+-----------+---------+----------------+------+-------------+
```
- 开启美国节点代理`python(python3) main.py -s 1`
- 打印节点列表`python(python3) main.py -l`
- 更新订阅列表`python(python3) main.py -u`
- 重置订阅链接`python(python3) main.py --setting-url https://tyrantlucifer.com/ssr/ssr.txt`
- 查看订阅链接列表`python(python3) main.py --list-url`
- 查看本地监听地址`python(python3) main.py --list-adderss`

## Linux终端设置代理方法

- 终端设置代理`export ALL_PROXY=socks5://127.0.0.1:1080`
- 查看代理是否设置成功`curl http://ip-api.com/json/?lang=zh-CN`
- 取消终端代理`unset ALL_PROXY`
- 如果想要更加方便的使用快捷命令，将以下内容添加到你家目录中的`.bashrc`中，然后执行`source ~/.bashrc`
```shell
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1080"
alias unsetproxy="unset ALL_PROXY"
alias ip="curl http://ip-api.com/json/?lang=zh-CN"
```
```angular2html
这样以下几个命令就会实现如下功能：

setproxy 开启代理
unsetproxy 关闭代理
ip 查看ip归属地
```

## 常见问题

- 我的代理打开了，为什么还是翻不出去？
> ssr-command-client的实质是使用Python版本的ssr开启了一个本地socks5代理，并没有实现自动分流和开启代理的功能，要想知道自己有没有开启成功，看上面使用方法章节，Linux学习如何命令行设置socks5代理，Windows学习如何在浏览器设置socks5代理

- 我的按照那几条命令查看了我的ip和设置了代理，都成功了，可是我执行`wget www.google.com`怎么还是不行？
> 命令行虽然设置好代理了，但是默认用的是我们本地的dns，没有用socks5代理的dns，国内早把google给污染了，google被解析到一个鬼一样的ip上，你说它咋能成功呢？你要是非要想用这种方法测试，使用curl --proxy socks5h://127.0.0.1:1080 www.google.com去查看是否有输出内容

- 针对Ubuntu Desktop用户的一些通知：
> 目前项目已经支持设置网络全局代理和pac代理，但是pac代理使用的file://协议指向的文件，新版chrome已经不支持这种协议的pac文件了，所以在设置完pac代理之后，chrome无法扶墙出去，但是火狐可以，如果chrome也想扶墙出去，建议使用SwitchyOmega插件进行分流，或者本地搭建一个http服务器，然后将`~/.ssr-command-client`下自动生成的autoproxy.pac扔到网站目录里去，在系统设置里把file://协议设置成http://协议即可

## 作者的几句话

> 1. ok，我开发这个东西是为了让自己服务器访问github的速度更加快一点而开发的，目的单纯是为了让coding更加顺畅一些。
> 2. 本客户端不适合小白用，需要有一些Linux基础或者有命令行终端使用经验的人来用，小白就不要来找我了好吗？
> 3. 我曾经写过几篇关于telegram的脚本和教程，但是不代表我会替人搭建或者买卖代理，小白也不要关注我公众号然后丢给我一句telegram代理、求telegram代理，我不是逗比，我没那个时间照顾小白情绪，不懂请绕路。
> 4. 因为最近工作和学习原因，公众号很少更新，流失了很多粉丝，但也无可奈何，希望大家能多多理解，不要取关，以后会更新更多精品内容。
> 5. `fork`的大哥们能否在`fork`之前给个`star`

## Tips

如果有好的建议，欢迎发邮件给我，或者关注下方我的个人微信公众号在后台留言，或者加qq群`764374820`反馈

- Email:Tyrantlucifer@gmail.com 
- Blog:https://tyrantlucifer.com
- Telegram:https://t.me/ssr_command_client
- Personal Wechat

![我的微信公众号](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/wechat.jpg)

## 致谢

感谢Jetbrains给予开发本项目的正版工具支持，如果有商业需求，推荐购买正版[Jetbrains](https://www.jetbrains.com/?from=ssr-command-client)
![Jetbrains](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/jetbrains-variant-2.png)
