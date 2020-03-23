# The command client of ShadowsocksR based Python3

在命令行下使用的一款ssr客户端

## 特性

- 支持订阅链接解析
- 支持多订阅链接解析
- 支持指定本地代理端口
- 支持节点测试ping值
- 自定义订阅链接
- 支持测试端口是否被tcp阻断

## ~~个人配置修改~~

~~修改项目中`conf.py`中的`UBSCRIBE_URL`为自己的订阅链接~~

全新版本已经移除`conf.py`，现支持命令行一键修改订阅链接，初始化设置为github共享订阅链接

## 安装方式

```shell

git clone https://github.com/TyrantLucifer/ssr-command-client.git
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
--add-url "add ssr subscribe url" 增加ssr订阅链接·
--remove-url "remove ssr subscribe url" 移除ssr订阅链接
--list-url "display ssr subscribe url" 显示当前ssr订阅链接
--list-address "display ssr local address" 显示当前ssr本地代理地址
--parse-url "parse ssr url" 解析ssr链接
--add-ssr "add ssr node" 添加ssr节点
--test-again ssr_node_id "test ssr node again" 重新测试节点延迟及端口状态
-v --version "display version" 显示当前版本
```

## 效果展示

- 输出ssr链接节点列表 python3 main.py -l，新版本的`ssr-command-client`更新列表需要`sudo`权限，如果以普通用户运行，请加`sudo`

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
- [ ] 支持Windows Linux双平台
- [ ] 支持自动生成PAC代理文件
- [ ] 支持一键关闭、开启系统PAC网络代理(针对于Ubuntu 18.04)

## Tips

如果有好的建议，欢迎发邮件给我，或者关注下方我的个人微信公众号在后台留言，或者加qq群`764374820`反馈

- Email:Tyrantlucifer@linuxstudy.cn
- Blog:www.linuxstudy.cn
- Personal Wechat

![我的微信公众号](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/wechat.jpg)


