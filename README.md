# The command client of ShadowsocksR based Python3

在命令行下使用的一款ssr客户端

**新版本已经更新，彻底摆脱root权限的烦恼**

## 特性

- 支持订阅链接解析
- 支持多订阅链接解析
- 支持指定本地代理端口
- 支持测试节点连接延迟
- 自定义订阅链接
- 支持测试端口是否被tcp阻断
- 支持设置开机自启
- 暂时不支持`ipv6`节点，默认解析节点时会进行屏蔽

## 安装方式

```shell
git clone https://github.com/TyrantLucifer/ssr-command-client.git
cd ssr-command-client
pip3 install -r requirement.txt
```

## 使用方法

```
python3 main.py [OPTIONS]

OPTIONS

-l --list "show ssr list" 展示ssr节点列表
-s --start "start ssr proxy" 启动ssr代理服务
-S --stop "stop ssr proxy" 停止ssr代理服务
-p --port port "assign local port" 指定本地代理端口
-c --config ssr_node_id "generate config json file" 生成指定节点json文件
-u --update "update ssr list" 更新ssr节点列表
--fast-node "generate fast ssr config json file" 生成最快节点json文件
--setting-url "set ssr subscribe url" 重置ssr订阅链接
--setting-address "set ssr local address" 设置ssr本地代理地址
--add-url "add ssr subscribe url" 增加ssr订阅链接
--remove-url "remove ssr subscribe url" 移除ssr订阅链接
--list-url "display ssr subscribe url" 显示当前ssr订阅链接
--list-address "display ssr local address" 显示当前ssr本地代理地址
--parse-url "parse ssr url" 解析ssr链接
--add-ssr "add ssr node" 添加ssr节点
--test-again ssr_node_id "test ssr node again" 重新测试节点延迟及端口状态
--setting-pac-proxy "setting system pac proxy,only support Ubuntu Desktop" 设置系统代理模式为pac代理，注：仅支持Ubuntu桌面系统
--setting-global-proxy "setting system global proxy,only support Ubuntu Desktop" 设置系统代理模式为全局代理，注：仅支持Ubuntu桌面系统
--close-system-proxy "close system proxy,only support Ubuntu Desktop" 关闭系统代理，注：仅支持Ubuntu桌面系统
--setting-auto-start "setting ssr auto start" 设置开机自启
-v --version "display version" 显示当前版本
```

## 效果展示

- 输出ssr链接节点列表 python3 main.py -l，~新版本的`ssr-command-client`更新列表需要`sudo`权限，如果以普通用户运行，请加`sudo`~，全新版本已经不再需要`root`权限

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200315024222.png)

- 更新ssr订阅链接 python3 main.py -u

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200315024425.png)

- 生成ssr节点配置文件 python3 main.py -c `ssr_node_id`

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200315023538.png)


- 启动ssr代理 python3 main.py -s

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200315023617.png)

- 停止ssr代理 python3 main.py -S

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200315023654.png)

## 更新ssr-command-client

``` shell
git pull
pip3 install -r requirement.txt
```


## Linux命令行设置代理方法

``` shell
export ALL_PROXY=socks5://127.0.0.1:1080 # 设置代理
unset ALL_PROXY # 关闭代理
curl http://ip-api.com/json/?lang=zh-CN # 查看当前ip归属地
```
如果想要方便的使用命令开关代理，可以将以下内容加入到自己的shell环境文件中：
``` shell
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1080"
alias unsetproxy="unset ALL_PROXY"
alias ip="curl http://ip-api.com/json/?lang=zh-CN"
```
这样下面这几个命令就会有以下功能：

`setproxy` 开启代理

`unsetproxy` 关闭代理

`ip` 查看ip归属地

## 未来计划

- [x] ~支持多订阅链接解析~
- [x] ~支持自动选择速度最优节点~
- [x] ~支持命令行解析ssr链接信息~
- [x] ~支持使用ssr链接添加节点~
- [x] ~支持自动生成PAC代理文件~
- [x] ~支持一键关闭、开启系统PAC网络代理(针对于Ubuntu 18.04)~
- [ ] 支持ipv6节点

## 常见问题

- 我的代理打开了，为什么还是翻不出去？

> ssr-command-client的实质是使用Python版本的ssr开启了一个本地socks5代理，并没有实现自动分流和开启代理的功能，要想知道自己有没有开启成功，看上面使用方法章节，学习如何命令行设置socks5代理

- 我的按照那几条命令查看了我的ip和设置了代理，都成功了，可是我执行`wget www.google.com`怎么还是不行？

> 命令行虽然设置好代理了，但是默认用的是我们本地的dns，没有用socks5代理的dns，国内早把google给污染了，google被解析到一个鬼一样的ip上，你说它咋能成功呢？你要是非要想用这种方法测试，使用`curl --proxy socks5h://127.0.0.1:1080 www.google.com`去查看是否有输出内容

- 针对Ubuntu桌面用户的一些通知

> 目前项目已经支持设置网络全局代理和pac代理，但是pac代理使用的`file://`协议指向的文件，新版chrome已经不支持这种协议的pac文件了，所以在设置完pac代理之后，chrome无法扶墙出去，但是火狐可以，如果chrome也想扶墙出去，建议使用`SwitchyOmega`插件进行分流，或者本地搭建一个http服务器，然后将项目目录下自动生成的autoproxy.pac扔到网站目录里去，在系统设置里把`file://`协议设置成`http://`协议即可

- 设置完开机自启之后，如何更加爽快的启动服务？

> (sudo) systemctl start ssr 启动ssr

> (sudo) systemctl stop ssr 停止ssr

> (sudo) systemctl restart ssr 重启ssr

- 作者的几句话

> 1. ok，我开发这个东西是为了让自己服务器访问github的速度更加快一点而开发的，目的单纯是为了让coding更加顺畅一些。

> 2. 本客户端不适合小白用，需要有一些Linux基础的人来用，小白就不要来找我了好吗？

> 3. 我曾经写过几篇关于`telegram`的脚本和教程，但是不代表我会替人搭建或者买卖代理，小白也不要关注我公众号然后丢给我一句`telegram代理`、`求telegram代理`，我不是逗比，我没那个时间照顾小白情绪，不懂请绕路。

> 4. 因为最近工作和学习原因，公众号很少更新，流失了很多粉丝，但也无可奈何，希望大家能多多理解。

> 5. `fork`的大哥们能否在`fork`之前给个`star` 

## Tips

如果有好的建议，欢迎发邮件给我，或者关注下方我的个人微信公众号在后台留言，或者加qq群`764374820`反馈

- Email:Tyrantlucifer@gmail.com
- Blog:https://tyrantlucifer.com
- Telegram:https://t.me/ssr_command_client
- Personal Wechat

![我的微信公众号](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/wechat.jpg)

